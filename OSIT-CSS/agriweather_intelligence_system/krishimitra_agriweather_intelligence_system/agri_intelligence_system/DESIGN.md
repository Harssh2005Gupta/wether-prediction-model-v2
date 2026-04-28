---
name: Agri-Intelligence System
colors:
  surface: '#f9f9f8'
  surface-dim: '#d9dad9'
  surface-bright: '#f9f9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f3'
  surface-container: '#edeeed'
  surface-container-high: '#e7e8e7'
  surface-container-highest: '#e1e3e2'
  on-surface: '#191c1c'
  on-surface-variant: '#42493e'
  inverse-surface: '#2e3131'
  inverse-on-surface: '#f0f1f0'
  outline: '#72796e'
  outline-variant: '#c2c9bb'
  surface-tint: '#3b6934'
  primary: '#154212'
  on-primary: '#ffffff'
  primary-container: '#2d5a27'
  on-primary-container: '#9dd090'
  inverse-primary: '#a1d494'
  secondary: '#006399'
  on-secondary: '#ffffff'
  secondary-container: '#67bafd'
  on-secondary-container: '#004972'
  tertiary: '#553112'
  on-tertiary: '#ffffff'
  tertiary-container: '#704727'
  on-tertiary-container: '#f0b78f'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#bcf0ae'
  primary-fixed-dim: '#a1d494'
  on-primary-fixed: '#002201'
  on-primary-fixed-variant: '#23501e'
  secondary-fixed: '#cde5ff'
  secondary-fixed-dim: '#94ccff'
  on-secondary-fixed: '#001d32'
  on-secondary-fixed-variant: '#004b74'
  tertiary-fixed: '#ffdcc5'
  tertiary-fixed-dim: '#f4bb92'
  on-tertiary-fixed: '#301400'
  on-tertiary-fixed-variant: '#653d1e'
  background: '#f9f9f8'
  on-background: '#191c1c'
  surface-variant: '#e1e3e2'
typography:
  headline-xl:
    fontFamily: Work Sans
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Work Sans
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Work Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Public Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-bold:
    fontFamily: Public Sans
    fontSize: 14px
    fontWeight: '700'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-md:
    fontFamily: Public Sans
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  caption:
    fontFamily: Public Sans
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 16px
  margin: 20px
  max-width: 1200px
---

## Brand & Style

The brand personality is rooted in the intersection of traditional wisdom and cutting-edge technology. It is **reliable** (providing consistent, data-driven insights), **intelligent** (leveraging AI for complex problem solving), **supportive** (acting as a digital companion in the field), and **grounded** (deeply connected to the literal earth and the farmers who work it).

The design style utilizes **Modern Corporate** with a **Tactile** twist. It prioritizes clarity and utility, using a structured card-based architecture that feels organized yet approachable. While the foundations are clean and professional, the UI incorporates subtle organic textures and depth to mimic the physical reality of agricultural work, ensuring the digital tool feels like a natural extension of the farmer's equipment.

## Colors

This design system uses a palette inspired by a thriving farm ecosystem. 

- **Primary (Forest Green):** Represents growth, health, and the core of the agricultural identity. Used for primary actions and brand presence.
- **Secondary (Sky Blue):** Symbolizes the expansive potential of AI and weather-dependent variables. Used for data visualizations and secondary interactive elements.
- **Tertiary (Warm Soil):** Grounds the interface in the reality of the land. Used for informational accents and organic dividers.
- **Neutral (Parchment/Fog):** A high-visibility, off-white base that reduces glare during outdoor use compared to pure white.
- **Alerts (Amber/Red):** High-chroma colors reserved strictly for critical crop alerts, pest warnings, or machinery malfunctions, ensuring they stand out against the earthy base tones.

## Typography

Typography is optimized for **outdoor legibility** and high-glare environments. 

**Work Sans** is used for headlines to provide a professional, sturdy presence with enough character to feel modern. Its slightly wider apertures ensure readability even on small mobile screens.

**Public Sans** is utilized for all body copy and labels. As a font designed for accessibility and clarity, it maintains exceptional legibility in long-form agricultural reports or quick-glance data dashboards. Line heights are intentionally generous to prevent text crowding, and font sizes start at a minimum of 16px for body content to accommodate users in active, mobile field environments.

## Layout & Spacing

The layout philosophy follows a **Fluid Grid** model with a strict 8px rhythmic scale. On mobile devices, a 4-column grid is used, expanding to 12 columns on tablet and desktop.

The "Card-First" approach dictates that content is grouped into logical modules. These cards use generous internal padding (typically `lg` or 24px) to ensure touch targets are easily hit, even when the user is wearing gloves or moving. White space is treated as a functional tool to separate distinct data points, preventing cognitive overload in high-pressure farming scenarios.

## Elevation & Depth

Visual hierarchy is established through **Tonal Layers** and **Ambient Shadows**. 

1.  **Base Layer:** The neutral background (#F8F9F8).
2.  **Card Layer:** Pure white surfaces with a soft, diffused shadow (12% opacity of the primary color) to provide a "lifted" effect that distinguishes interactive modules from the background.
3.  **Active/Modal Layer:** Higher elevation shadows with a slightly larger blur radius to indicate temporary focus or urgent AI prompts.

Low-contrast outlines in the Soil tone (#8B5E3C at 15% opacity) are used on card borders to provide structural definition without adding visual noise, ensuring the cards feel integrated into the "ground" of the app.

## Shapes

The design system utilizes **Rounded (Level 2)** geometry. Standard UI elements like buttons and input fields feature a 0.5rem (8px) corner radius. This strikes a balance between the precision of technology and the organic curves found in nature.

Larger containers and cards use `rounded-lg` (1rem / 16px) to soften the overall appearance of the interface, making the AI feel supportive and approachable rather than cold or industrial. Icons are contained within circular or highly rounded backgrounds to maintain a consistent language of "soft-utility."

## Components

-   **Cards:** The primary container. Cards should have a white background, `rounded-lg` corners, and a subtle ambient shadow. They must include a clear header and a footer for primary actions.
-   **Buttons:** 
    -   *Primary:* Solid Forest Green with white text. High contrast, large touch area (min height 48px).
    -   *Secondary:* Outlined Sky Blue for non-critical navigation or filtering.
-   **Data Visualizations:** Use Sky Blue for "ideal" ranges and Forest Green for "actual" data. Use Amber for "caution" zones. Charts should be simplified with minimal grid lines to emphasize trends over granular points.
-   **Status Chips:** Small, pill-shaped indicators for "Soil Moisture," "Pest Level," or "Growth Stage." Use high-contrast text on desaturated background tints of the status color.
-   **Input Fields:** Heavily defined borders using the Soil tone to ensure they are visible in bright sunlight. Labels must always be visible (no floating labels that disappear).
-   **AI Insight Toast:** A specific component with a subtle Sky Blue gradient border and a unique "Spark" icon to denote an intelligence-driven suggestion.