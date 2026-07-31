#!/usr/bin/env python3
"""
Exact solver for federal grant budget personnel from fixed categories and MTDC equation.

Usage: Edit the fixed values below, then run this script. It finds the exact Personnel (P)
such that Total = target ceiling, handling rounding to whole dollars.

The MTDC equation:
  Total = 1.472P + fixed + 0.15 * mtdc_fixed
  P = (Total - fixed - 0.15 * mtdc_fixed) / 1.472

Where:
  fixed = Travel + Supplies + Equipment + Contractual + OtherDirect_Total
  mtdc_fixed = Travel + Supplies + (num_subs * 50000) + OtherDirect_Services
"""


def solve_budget(
    target_total,
    travel,
    supplies,
    equipment,
    contractual,
    od_services,
    od_participant,
    num_subawards,
    fringe_rate=0.28,
    indirect_rate=0.15,
):
    """Solve for exact Personnel given fixed budget categories."""
    od_total = od_services + od_participant
    fixed = travel + supplies + equipment + contractual + od_total
    subs_in_mtdc = num_subawards * 50000
    mtdc_fixed = travel + supplies + subs_in_mtdc + od_services

    # Closed-form solution
    # Total = 1.472P + fixed + 0.15*mtdc_fixed  (when fringe=0.28, indirect=0.15)
    coef = 1 + fringe_rate + fringe_rate * indirect_rate + indirect_rate
    P_exact = (target_total - fixed - indirect_rate * mtdc_fixed) / coef

    print(f"Target total:    ${target_total:,.0f}")
    print(f"Fixed categories: ${fixed:,}")
    print(f"MTDC fixed:      ${mtdc_fixed:,}")
    print(f"Exact P:         ${P_exact:,.2f}")
    print()

    # Search around exact P for rounding-compatible solution
    for P in range(int(P_exact) - 50, int(P_exact) + 50):
        fringe = round(P * fringe_rate)
        direct = P + fringe + travel + supplies + equipment + contractual + od_total
        mtdc = P + fringe + travel + supplies + subs_in_mtdc + od_services
        indirect = round(indirect_rate * mtdc)
        total = direct + indirect

        if total == target_total:
            print("=" * 65)
            print("SOLUTION FOUND (zero delta):")
            print(f"  A. Personnel:      ${P:>14,}")
            print(f"  B. Fringe ({fringe_rate*100:.1f}%):  ${fringe:>14,}")
            print(f"  C. Travel:         ${travel:>14,}")
            print(f"  D. Equipment:      ${equipment:>14,}")
            print(f"  E. Supplies:       ${supplies:>14,}")
            print(f"  F. Contractual:    ${contractual:>14,}  ({num_subawards} subawards × $50K = ${subs_in_mtdc:,} in MTDC)")
            print(f"  H. Other Direct:   ${od_total:>14,}  (Services: ${od_services:,} + Participant: ${od_participant:,})")
            print(f"  I. TOTAL DIRECT:   ${direct:>14,}")
            print(f"  MTDC BASE:         ${mtdc:>14,}")
            print(f"  J. INDIRECT:       ${indirect:>14,}  ({indirect_rate*100:.0f}% of MTDC)")
            print(f"  K. GRAND TOTAL:    ${total:>14,}")
            print(f"  Delta from target: ${total - target_total}")
            print("=" * 65)

            # Personnel allocation guidance
            annual_personnel = P / 2
            print(f"\nAnnual personnel budget: ${annual_personnel:,.0f}")
            print(f"Typical 9-10 position allocation for ~${P:,.0f} over 24 months:")
            return {
                "personnel": P,
                "fringe": fringe,
                "direct": direct,
                "mtdc": mtdc,
                "indirect": indirect,
                "total": total,
                "delta": total - target_total,
            }

    # No exact solution found; show closest
    print("No exact solution found. Closest candidates:")
    for P in range(int(P_exact) - 5, int(P_exact) + 5):
        fringe = round(P * fringe_rate)
        direct = P + fringe + travel + supplies + equipment + contractual + od_total
        mtdc = P + fringe + travel + supplies + subs_in_mtdc + od_services
        indirect = round(indirect_rate * mtdc)
        total = direct + indirect
        print(f"  P={P:,} → Total=${total:,} (Δ={total-target_total})")

    return None


if __name__ == "__main__":
    # --- EDIT THESE VALUES ---
    TARGET_TOTAL = 5_901_000
    TRAVEL = 420_000
    SUPPLIES = 160_000
    EQUIPMENT = 150_000
    CONTRACTUAL = 1_800_000  # Total of all subawards
    OD_SERVICES = 500_000     # Cloud, software, translation, venues, audit (MTDC-eligible)
    OD_PARTICIPANT = 120_000  # Participant support (EXCLUDED from MTDC)
    NUM_SUBAWARDS = 3         # Each contributes first $50K to MTDC
    FRINGE_RATE = 0.28
    INDIRECT_RATE = 0.15      # 15% de minimis per 2 CFR 200.414(f)

    solve_budget(
        target_total=TARGET_TOTAL,
        travel=TRAVEL,
        supplies=SUPPLIES,
        equipment=EQUIPMENT,
        contractual=CONTRACTUAL,
        od_services=OD_SERVICES,
        od_participant=OD_PARTICIPANT,
        num_subawards=NUM_SUBAWARDS,
        fringe_rate=FRINGE_RATE,
        indirect_rate=INDIRECT_RATE,
    )