# GovCon Contact Section Pattern

## User-Settled Format (Leatherneck Federal Consulting)

The user iterated through several versions of the contact section. The final settled format:

```
LOCATION:    Lexington, South Carolina    (city/state only — NO street address)
ENTITY:      SC LLC · DVOSB · UEI: VU2HV8458J93 · CAGE: 21BA0
CERTS:       PMP · DAWIA Level III (1102) · CMMC L2 (in process)
PHONE:       803-904-3500    (single number only — no multiple lines)
ESTABLISHED: 2026            (year only)
```

## Design Decisions

| Element | Included? | Rationale |
|---------|-----------|-----------|
| Street address | **No** | User explicitly removed. City/state is sufficient for public site; full address is in SAM.gov. |
| EIN | **No** | User replaced with UEI + CAGE. EIN is sensitive; UEI/CAGE are the identifiers evaluators actually cross-reference. |
| Multiple phone numbers | **No** | User explicitly removed secondary numbers. Single contact number is cleaner. |
| UEI + CAGE | **Yes** | These are the primary SAM.gov identifiers evaluators verify against. |
| SDVOSB/VetCert language | **Minimal** | Use "DVOSB" not "SDVOSB (self-attested) · VetCert in process." The verbose self-attestation/VetCert language was removed. |
| Standard certs | **Yes** | PMP, DAWIA Level III, and CMMC-related certs signal domain competence to contracting officers. |

## Contact Email

The user settled on `inquiries@leatherneckconsulting.com` as the public-facing email (not individual principal emails). Individual email addresses (e.g., DouglasHenderson@) may appear in privately-shared capabilities statements but not on the public website.

## Footer Pattern

Minimal, matches the contact section:
```
SC LLC · DVOSB · Est. 2026
```
No "self-attested" language, no VetCert status, no EIN, no UEI/CAGE (those are in the contact section).

## Render Pattern (Next.js + Tailwind)

The contact section uses a dark `.band-navy` background with gold section labels and white text. Each field is a `<div>` with a label in tiny gold tracking font and the value below:

```tsx
<div className="space-y-6 text-[#A7B0C4]">
  <div>
    <div className="font-heading text-[10px] tracking-[0.3em] text-[#C9A227]">LOCATION</div>
    <div className="text-lg text-white">Lexington, South Carolina</div>
  </div>
  {/* ... ENTITY, CERTS, PHONE, ESTABLISHED ... */}
</div>
```
