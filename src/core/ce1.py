#!/usr/bin/env python3
"""
CE1 CurvatureModeKernel (seed recorded in this docstring): seed=ce1_v1_2025-09-02

Implements CE1{
  lens=Kaleidoscope[pascal_dihedral; facets=F]
  mode=CurvatureModeKernel
  Ω=LockAngle(critical_line,0.5)

  inputs={ actions A={(s,r)}, scores g[A], polygon=RegularFgon(F), grid=SurfaceGrid(res=R) }
  params={ scales σ=[σ0,σ1,σ2], gamma=γ, mate_map=MATE((s,r)), compress=asinh }
  emit: CE1v{ surfaces, overlays, palette, annotations }
"""

from __future__ import annotations

import argparse
import os
import time
import math
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from rh import (
    RHIntegerAnalyzer,
    PascalKernel,
    IntegerSandwich,
    NTTProcessor,
    mate,
)
from rh import QuantitativeGapAnalyzer
from matplotlib import pyplot as plt


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _makedirs(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _regular_polygon(F: int, radius: float = 1.0) -> np.ndarray:
    angles = np.linspace(0.0, 2.0 * math.pi, F, endpoint=False)
    return np.stack([radius * np.cos(angles), radius * np.sin(angles)], axis=1)


def _point_in_poly_mask(poly_xy: np.ndarray, grid: Tuple[int, int], margin: float = 0.05) -> Tuple[np.ndarray, Tuple[float, float, float, float]]:
    # Compute a tight AABB and rasterize using winding test
    F = poly_xy.shape[0]
    xs = poly_xy[:, 0]
    ys = poly_xy[:, 1]
    xmin, xmax = float(xs.min()), float(xs.max())
    ymin, ymax = float(ys.min()), float(ys.max())
    sx = xmax - xmin
    sy = ymax - ymin
    xmin -= margin * sx
    xmax += margin * sx
    ymin -= margin * sy
    ymax += margin * sy

    H, W = grid
    yy = np.linspace(ymin, ymax, H)
    xx = np.linspace(xmin, xmax, W)
    X, Y = np.meshgrid(xx, yy)

    # Vectorized crossing number algorithm
    mask = np.zeros((H, W), dtype=bool)
    x = X
    y = Y
    for i in range(F):
        x0, y0 = poly_xy[i]
        x1, y1 = poly_xy[(i + 1) % F]
        cond = ((y0 <= y) & (y < y1)) | ((y1 <= y) & (y < y0))
        x_int = x0 + (y - y0) * (x1 - x0) / ((y1 - y0) + 1e-12)
        mask ^= cond & (x < x_int)
    return mask, (xmin, xmax, ymin, ymax)


def _gaussian_kernel2d(sigma: float, radius: Optional[int] = None) -> np.ndarray:
    if sigma <= 0:
        return np.array([[1.0]], dtype=np.float64)
    if radius is None:
        radius = max(1, int(math.ceil(3.0 * sigma)))
    ax = np.arange(-radius, radius + 1, dtype=np.float64)
    xx, yy = np.meshgrid(ax, ax)
    g = np.exp(-(xx * xx + yy * yy) / (2.0 * sigma * sigma))
    g /= g.sum() or 1.0
    return g


def _convolve2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    # Simple valid-sized FFT-based convolution with same output size (reflect padding)
    if kernel.size == 1:
        return image.copy()
    pad_y = kernel.shape[0] // 2
    pad_x = kernel.shape[1] // 2
    padded = np.pad(image, ((pad_y, pad_y), (pad_x, pad_x)), mode="reflect")
    out = np.zeros_like(image, dtype=np.float64)
    # Separable if Gaussian; but we keep generic for Dx,Dy, etc.
    # Use direct convolution for simplicity and clarity here (small kernels).
    kh, kw = kernel.shape
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            window = padded[i:i+kh, j:j+kw]
            out[i, j] = float(np.sum(window * kernel))
    return out


def _derive_gaussian_kernels(sigma: float) -> Dict[str, np.ndarray]:
    r = max(1, int(math.ceil(3.0 * sigma))) if sigma > 0 else 1
    ax = np.arange(-r, r + 1, dtype=np.float64)
    # 1D Gaussian and derivatives
    g1 = np.exp(-(ax * ax) / (2.0 * sigma * sigma)) if sigma > 0 else np.array([1.0])
    if g1.ndim == 1:
        pass
    g1 /= g1.sum() or 1.0
    if sigma > 0:
        dg = -(ax / (sigma * sigma)) * g1
        ddg = ((ax * ax - sigma * sigma) / (sigma ** 4)) * g1
    else:
        dg = np.array([0.0])
        ddg = np.array([0.0])

    G = np.outer(g1, g1)
    Dx = np.outer(g1, dg)
    Dy = np.outer(dg, g1)
    Dxx = np.outer(g1, ddg)
    Dyy = np.outer(ddg, g1)
    Dxy = np.outer(dg, dg)
    return {"G": G, "Dx": Dx, "Dy": Dy, "Dxx": Dxx, "Dyy": Dyy, "Dxy": Dxy}


def _principal_curvatures(Hxx: np.ndarray, Hyy: np.ndarray, Hxy: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    trace = Hxx + Hyy
    det = Hxx * Hyy - Hxy * Hxy
    disc = np.maximum(0.0, trace * trace - 4.0 * det)
    sqrt_disc = np.sqrt(disc)
    k1 = 0.5 * (trace + sqrt_disc)
    k2 = 0.5 * (trace - sqrt_disc)
    return k1, k2


def _asinh_compress(x: Any) -> np.ndarray:
    arr = np.asarray(x, dtype=np.float64)
    return np.arcsinh(arr)


def _write_ce1v(path: str, payload: Dict[str, Any]) -> None:
    lines: List[str] = []
    lines.append("CE1v{\n")
    lines.append("  surfaces={\n")
    lines.append(f"    height={payload['surfaces']['height']},\n")
    lines.append(f"    emboss={payload['surfaces']['emboss']},\n")
    lines.append("  },\n")
    lines.append("  overlays={\n")
    lines.append(f"    ridges={payload['overlays']['ridges']},\n")
    lines.append(f"    valleys={payload['overlays']['valleys']},\n")
    lines.append(f"    lock={payload['overlays']['lock']},\n")
    lines.append("  },\n")
    lines.append("  palette={height:\"viridis\", emboss:\"magma\"},\n")
    Fv = payload['annotations']['F']
    Nv = payload['annotations']['N']
    Tv = payload['annotations']['t_approx']
    Gv = payload['annotations']['gamma']
    lines.append(f"  annotations={{{{F={Fv}, N={Nv}, t≈={Tv}, gamma={Gv}}}}}\n")
    lines.append("}\n")
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(lines))


def _compute_exact_scores(mask: List[int], template: List[int], N: int) -> Tuple[int, int, int, int, int]:
    _require(N > 0, "N must be > 0")
    _require(len(mask) == N and len(template) == N, "mask/template size mismatch")
    A_pad, V_pad, N_pad = IntegerSandwich._prepare_ntt_arrays(mask, template, N)
    mod = 2**31 - 1
    ntt = NTTProcessor(N_pad)
    A_ntt = ntt.ntt(A_pad)
    V_ntt = ntt.ntt(V_pad)
    V_rev = V_pad[::-1]
    V_rev_ntt = ntt.ntt(V_rev)
    rot_prod = [(x * y) % mod for x, y in zip(A_ntt, V_rev_ntt)]
    ref_prod = [(x * y) % mod for x, y in zip(A_ntt, V_ntt)]
    rotations = ntt.intt(rot_prod)[:N]
    reflections = ntt.intt(ref_prod)[:N]
    all_scores = rotations + reflections
    winner_idx = int(all_scores.index(max(all_scores)))
    winner_score = int(all_scores[winner_idx])
    is_reflection = winner_idx >= N
    shift = winner_idx % N
    mate_shift, mate_ref = mate(shift, is_reflection, N)
    mate_idx = mate_shift + (N if mate_ref else 0)
    rival = [all_scores[i] for i in range(len(all_scores)) if i != winner_idx and i != mate_idx]
    runner_up_score = int(max(rival)) if rival else int(winner_score)
    gap = int(winner_score - runner_up_score)
    runner_up_idx = int(all_scores.index(runner_up_score))
    return winner_idx, runner_up_idx, winner_score, runner_up_score, gap


def run_curvature_mode(
    *,
    depth: int,
    facets: int,
    grid_res: int,
    sigma_list: List[float],
    gamma: float,
    zero_t: float,
) -> Dict[str, Any]:
    analyzer = RHIntegerAnalyzer(depth=depth)
    N = analyzer.N
    kernel = PascalKernel(N, depth)

    # Lock at Ω = (1/2, t≈zero)
    zeros_meta = [0.5 + 1j * zero_t]
    anchor = analyzer.analyze_point_metanion(complex(0.5, zero_t), zeros_meta)
    best = anchor["best_action"]
    locked_shift = int(best.shift)

    # Build a representative mask/template at lock point (on-line)
    # Use QuantitativeGapAnalyzer helper consistently
    qga = QuantitativeGapAnalyzer()
    mask, template = qga.create_e_n_based_mask(sigma=0.5, t=zero_t, N=N, zeros=zeros_meta, kernel=kernel)

    # Create regular polygon facet stencil and raster grid
    poly = _regular_polygon(facets, radius=1.0)
    mask_poly, aabb = _point_in_poly_mask(poly, (grid_res, grid_res))

    # Splat actions to surface: interpret action scores via exact integer sandwich
    w_idx, r_idx, w_score, r_score, gap = _compute_exact_scores(mask, template, N)
    # Build 2N action scores array via correlator-once more? Reuse rotations/reflections from exact computation above.
    # We already computed the sequences; reconstruct per-action scores to splat
    # For simplicity, we approximate by a single strong impulse at the locked facet bin.
    S = np.zeros((grid_res, grid_res), dtype=np.float64)
    # Map locked shift to facet index
    locked_facet = int((facets * locked_shift) // N)
    # Paint a filled polygon region scaled by score
    S[mask_poly] = float(w_score)

    # Multi-scale smoothing and curvature primitives
    H_blends: List[np.ndarray] = []
    K_blends: List[np.ndarray] = []
    ridge_masks: List[np.ndarray] = []
    valley_masks: List[np.ndarray] = []
    for sigma in sigma_list:
        kers = _derive_gaussian_kernels(float(sigma))
        S_s = _convolve2d(S, kers["G"])  # smoothed
        S_x = _convolve2d(S, kers["Dx"])  # first derivatives
        S_y = _convolve2d(S, kers["Dy"])  # first derivatives
        S_xx = _convolve2d(S, kers["Dxx"])  # Hessian terms
        S_yy = _convolve2d(S, kers["Dyy"])  # Hessian terms
        S_xy = _convolve2d(S, kers["Dxy"])  # Hessian terms
        k1, k2 = _principal_curvatures(S_xx, S_yy, S_xy)
        H = 0.5 * (k1 + k2)
        K = k1 * k2
        H_blends.append(H)
        K_blends.append(K)
        # Thresholds per-scale via robust statistic
        tau = float(np.percentile(np.abs(k1), 90.0)) or 0.0
        ridge = (k1 > 0) & (np.abs(k1) >= tau)
        valley = (k2 < 0) & (np.abs(k2) >= tau)
        ridge_masks.append(ridge)
        valley_masks.append(valley)

    # Blend scales coarse→fine weights [1, 1/2, 1/4, ...]
    weights = [1.0 / (2.0 ** i) for i in range(len(H_blends))]
    wsum = sum(weights) or 1.0
    H_fused = sum(w * H for w, H in zip(weights, H_blends)) / wsum
    K_fused = sum(w * K for w, K in zip(weights, K_blends)) / wsum
    ridges = np.logical_or.reduce(ridge_masks) if ridge_masks else np.zeros_like(S, dtype=bool)
    valleys = np.logical_or.reduce(valley_masks) if valley_masks else np.zeros_like(S, dtype=bool)

    # Compress for output
    H_comp = _asinh_compress(H_fused)
    K_comp = _asinh_compress(K_fused)

    # Build lock badge from exact scoring
    is_reflection = (w_idx >= N)
    s_shift = int(w_idx % N)
    lock_tuple = (s_shift, bool(is_reflection))
    gamma_int = int(round(float(gamma)))
    passed = (int(w_score) >= gamma_int) and (int(w_score - r_score) >= 1)

    # Serialize compactly: store minified arrays as Python-like repr for CE1v writer
    def arr_to_str(a: np.ndarray) -> str:
        # Downsample for compact emission if very large
        Hh, Ww = a.shape
        max_side = 96
        scale = max(1, int(max(Hh, Ww) // max_side))
        if scale > 1:
            a_small = a[::scale, ::scale]
        else:
            a_small = a
        flat = a_small.astype(np.float64).ravel()
        # clip to 6 decimals
        return "[" + ", ".join(f"{float(x):.6f}" for x in flat.tolist()) + "]"

    payload = {
        "surfaces": {
            "height": arr_to_str(H_comp),
            "emboss": arr_to_str(K_comp),
        },
        "overlays": {
            "ridges": arr_to_str(ridges.astype(np.float32)),
            "valleys": arr_to_str(valleys.astype(np.float32)),
            "lock": str(lock_tuple),
        },
        "annotations": {
            "F": int(facets),
            "N": int(N),
            "t_approx": float(zero_t),
            "gamma": int(gamma_int),
        },
    }

    return {
        "payload": payload,
        "scores": {
            "winner_idx": int(w_idx),
            "runner_idx": int(r_idx),
            "winner": int(w_score),
            "runner": int(r_score),
            "gap": int(gap),
        },
        # Provide raw arrays for optional rendering
        "arrays": {
            "H": H_fused,
            "K": K_fused,
            "ridges": ridges,
            "valleys": valleys,
        },
    }


def _render_surface_overlays_png(
    H: np.ndarray,
    K: np.ndarray,
    ridges: np.ndarray,
    valleys: np.ndarray,
    out_png: str,
    title: str,
    palette_h: str = "viridis",
    palette_k: str = "magma",
) -> bool:
    try:
        fig = plt.figure(figsize=(10, 5), dpi=180)
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        fig.suptitle(title)
        for ax in (ax1, ax2):
            ax.axis('off')
        # Normalize helper
        def norm_img(a: np.ndarray) -> np.ndarray:
            a = a.astype(np.float64)
            lo, hi = np.percentile(a, [2.0, 98.0])
            denom = (hi - lo) if hi > lo else 1.0
            return np.clip((a - lo) / denom, 0.0, 1.0)
        ax1.imshow(norm_img(H), cmap=plt.get_cmap(palette_h), origin='lower')
        ax1.set_title("height (H)")
        ax2.imshow(norm_img(K), cmap=plt.get_cmap(palette_k), origin='lower')
        ax2.set_title("emboss (K)")
        # Overlays
        yy, xx = np.nonzero(ridges)
        if yy.size > 0:
            ax1.scatter(xx, yy, s=1.0, c="#ff2d2d", alpha=0.7, linewidths=0)
            ax2.scatter(xx, yy, s=1.0, c="#ff2d2d", alpha=0.7, linewidths=0)
        yy, xx = np.nonzero(valleys)
        if yy.size > 0:
            ax1.scatter(xx, yy, s=1.0, c="#2ddaff", alpha=0.7, linewidths=0)
            ax2.scatter(xx, yy, s=1.0, c="#2ddaff", alpha=0.7, linewidths=0)
        fig.tight_layout()
        fig.savefig(out_png)
        plt.close(fig)
        return True
    except Exception:
        return False


def main() -> int:
    p = argparse.ArgumentParser(description="CE1 CurvatureModeKernel")
    p.add_argument("--depth", type=int, default=4, help="Pascal depth (N=2^depth+1)")
    p.add_argument("--facets", type=int, default=12, help="Polygon facets F")
    p.add_argument("--grid", type=int, default=192, help="Surface grid resolution (square)")
    p.add_argument("--sigmas", type=str, default="1,2,4", help="Comma-separated Gaussian scales")
    p.add_argument("--gamma", type=float, default=5.0, help="Detection threshold gamma")
    p.add_argument("--zero", type=float, default=14.134725, help="Imag part t of target zero")
    p.add_argument("--out", type=str, default=".out/ce1", help="Output directory")
    p.add_argument("--png", action="store_true", help="Render PNG image with overlays")
    args = p.parse_args()

    sigmas = [float(s.strip()) for s in str(args.sigmas).split(",") if s.strip()]
    _require(len(sigmas) > 0, "need at least one sigma")
    _require(args.facets >= 3, "facets must be >= 3")
    _require(args.grid >= 16, "grid must be >= 16")

    res = run_curvature_mode(
        depth=int(args.depth),
        facets=int(args.facets),
        grid_res=int(args.grid),
        sigma_list=sigmas,
        gamma=float(args.gamma),
        zero_t=float(args.zero),
    )

    _makedirs(args.out)
    ts = time.strftime("%Y%m%d-%H%M%S")
    base = f"ce1-curv-depth{args.depth}-F{args.facets}-grid{args.grid}-t{args.zero:.6f}-{ts}"
    out_ce1v = os.path.join(args.out, f"{base}.ce1v")

    _write_ce1v(out_ce1v, res["payload"]) 
    print(f"Wrote CE1v: {out_ce1v}")
    sc = res["scores"]
    print(f"Winner idx: {sc['winner_idx']} score={sc['winner']} runner={sc['runner']} gap={sc['gap']}")
    if args.png:
        arr = res.get("arrays", {})
        H = arr.get("H")
        ridges = arr.get("ridges")
        valleys = arr.get("valleys")
        K = arr.get("K")
        if isinstance(H, np.ndarray) and isinstance(K, np.ndarray) and isinstance(ridges, np.ndarray) and isinstance(valleys, np.ndarray):
            out_png = os.path.join(args.out, f"{base}.png")
            ok = _render_surface_overlays_png(H, K, ridges, valleys, out_png, title=f"CE1 Curvature F={args.facets} N≈{2**args.depth+1}")
            if ok and os.path.exists(out_png):
                print(f"Wrote PNG: {out_png}")
            else:
                print("PNG render failed (matplotlib or runtime error)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


