# Design System: The Gilded Plum

This design system defines the visual guidelines and tokens for **The Gilded Plum**. All components and sections must adhere to these tokens to ensure branding integrity and aesthetic consistency.

## Color Palette

- **Primary:** `#d4af37` (Gold) — used for main actions, key UI elements
- **Secondary:** `#f1d592` (Light Gold) — used for supporting elements, secondary buttons
- **Background:** `#000000` (Pure Black) — main canvas color
- **Surface:** `#121212` (Dark Charcoal) — cards, modals, elevated elements
- **Text Primary:** `#f5eedf` (Warm Gold Cream) — headings, body copy
- **Text Secondary:** `#a69e94` (Muted Gold Gray) — captions, helper text, placeholders
- **Border:** `rgba(212, 175, 55, 0.15)` — dividers, input outlines
- **Success:** `#2e7d32`
- **Warning:** `#e65100`
- **Error:** `#c62828`

## Typography

- **Font Family (Headings):** `'Playfair Display', serif`
- **Font Family (Body):** `'Source Sans 3', sans-serif`
- **Headings:** bold, tracking tight (`letter-spacing: -0.02em`)
- **Body:** regular weight (`font-weight: 400`)
- **Size Scale:** 
  - `12px` (0.75rem)
  - `14px` (0.875rem)
  - `16px` (1rem)
  - `20px` (1.25rem)
  - `24px` (1.5rem)
  - `32px` (2rem)
  - `40px` (2.5rem)
  - `48px` (3rem)

## Spacing Scale

Use a 4px base unit. Common values:
- `4px` (0.25rem)
- `8px` (0.5rem)
- `12px` (0.75rem)
- `16px` (1rem)
- `24px` (1.5rem)
- `32px` (2rem)
- `48px` (3rem)
- `64px` (4rem)

## Border Radius

- **Small (inputs, chips):** `4px`
- **Medium (cards, buttons):** `8px`
- **Large (modals, containers):** `12px`
- **Full (avatars, pills):** `9999px`

## Shadows

- **Subtle:** `0 1px 2px rgba(0,0,0,0.05)`
- **Medium:** `0 4px 12px rgba(0,0,0,0.1)`
- **Strong:** `0 8px 24px rgba(0,0,0,0.15)`

## Component Patterns

- **Buttons:** 
  - Padding: `12px 24px` (0.75rem 1.5rem)
  - Height: `48px` (3rem)
  - Hover States: Scale transition (`transform: scale(0.98)` or hover gold translation), smooth border transition
- **Inputs:** 
  - Height: `48px` (3rem)
  - Padding: `12px 16px` (0.75rem 1rem)
  - Focus States: Outlines with primary gold color, subtle glowing box-shadow
- **Cards:** 
  - Padding: `24px` (1.5rem)
  - Shadow: Medium
  - Border Treatment: `1px solid rgba(212, 175, 55, 0.1)`, radius Medium

## Rules

1. **Never introduce colors outside this palette.**
2. **Always use the spacing scale — no arbitrary values.**
3. **Maintain consistent border radius per element type.**
