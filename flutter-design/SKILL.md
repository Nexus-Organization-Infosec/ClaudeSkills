---
name: flutter-design
description: Design and build polished Flutter UI for Android following Material 3 (Material You) — correct theming with ColorScheme.fromSeed, dynamic color, the modern M3 component set (NavigationBar, FilledButton, SegmentedButton, etc.), the M3 type scale, shape/elevation/spacing tokens, dark mode, adaptivity, and accessibility. Use whenever the user invokes /flutter-design or asks to "build a Flutter screen/UI", "make this look like Material 3 / Material You", "design an Android app UI in Flutter", "theme my Flutter app", or "make my Flutter widgets look good". Produces UI that reads as one coherent, modern Material system rather than default-widget soup.
---

# Flutter Design — Material 3 for Android

Build Flutter UI that looks like a real, modern Android app: coherent color, proper Material 3 components, consistent spacing and shape, dark mode, and accessible touch targets. The difference between "default widgets thrown on a screen" and a designed app is almost entirely **theming discipline** — colors, type, and shape driven from one system, never hardcoded per-widget.

## 1. Set up the theme once (the foundation)

Everything flows from a single `ColorScheme` seeded from a brand color, with a matching dark scheme, and dynamic color on Android 12+ (Material You pulls colors from the user's wallpaper). Material 3 is the default in current Flutter, but set it explicitly.

```dart
class AppTheme {
  static const seed = Color(0xFF6750A4); // your brand color; dynamic color overrides on Android 12+

  static ThemeData _base(ColorScheme scheme) =>
      ThemeData(useMaterial3: true, colorScheme: scheme);

  static ThemeData light([ColorScheme? dyn]) =>
      _base(dyn ?? ColorScheme.fromSeed(seedColor: seed));
  static ThemeData dark([ColorScheme? dyn]) =>
      _base(dyn ?? ColorScheme.fromSeed(seedColor: seed, brightness: Brightness.dark));
}

// main.dart — wire dynamic color + system light/dark:
DynamicColorBuilder(
  builder: (lightDynamic, darkDynamic) => MaterialApp(
    theme: AppTheme.light(lightDynamic?.harmonized()),
    darkTheme: AppTheme.dark(darkDynamic?.harmonized()),
    themeMode: ThemeMode.system,
    home: const HomeScreen(),
  ),
);
```

`DynamicColorBuilder` needs the `dynamic_color` package; the `?? ColorScheme.fromSeed(...)` fallback means it still looks right on older devices / other platforms.

## 2. Use the M3 component set (not the old ones)

Reach for the modern widgets — they carry the M3 look for free:

| Use this (M3) | Instead of |
|---|---|
| `NavigationBar` | `BottomNavigationBar` |
| `NavigationRail` / `NavigationDrawer` | ad-hoc side menus |
| `FilledButton`, `FilledButton.tonal` | most `ElevatedButton` uses |
| `SegmentedButton` | `ToggleButtons` |
| `SearchAnchor` / `SearchBar` | a `TextField` styled as search |
| `Card.filled` / `Card.outlined` | shadow-heavy custom cards |
| `MenuAnchor` / `DropdownMenu` | old `PopupMenuButton`/`DropdownButton` |
| `Badge`, `Chip` variants (`FilterChip`, `InputChip`, `ActionChip`) | custom pills |

Buttons hierarchy: **FilledButton** = primary action, **tonal** = secondary emphasis, **OutlinedButton** = medium, **TextButton** = low. One primary filled button per view.

## 3. Design tokens — pull everything from the theme

- **Color: use `ColorScheme` roles, never raw hex.** `colorScheme.primary` / `onPrimary`, `secondary`, `tertiary`, `surface`, `surfaceContainer` (…`Lowest`/`Low`/`High`/`Highest` for layered surfaces), `onSurface`, `onSurfaceVariant` (secondary text), `outline`/`outlineVariant` (borders/dividers), `error`. Access via `final cs = Theme.of(context).colorScheme;`. This is what makes light/dark and dynamic color "just work."
- **Typography: use the M3 type scale**, never bare `TextStyle(fontSize: …)`. `Theme.of(context).textTheme.headlineMedium` / `titleLarge` / `bodyLarge` / `labelLarge` etc. Recolor with `.copyWith(color: cs.onSurfaceVariant)` when needed.
- **Shape:** M3 favors rounded corners — cards/sheets ~12–16, small elements ~8, FAB ~16, full-stadium for chips/pills. Prefer the component defaults; theme globally via `cardTheme`, `chipTheme` if you must.
- **Elevation:** M3 leans on **tonal elevation** (surface tint / `surfaceContainer` layers) more than big drop shadows. Keep shadows subtle; differentiate layers with surface-container roles.

## 4. Spacing & layout

- **8dp grid.** Use multiples of 4/8 for padding and gaps (`8, 12, 16, 24`). Default screen padding ~16.
- Group related content; use whitespace, not dividers, as the first tool for separation (`outlineVariant` dividers only when needed).
- Wrap scrollable/edge content in `SafeArea`; use `ListView`/`SliverList` for long content, not a `Column` in a `SingleChildScrollView` for big lists.

## 5. Adaptivity (phones → tablets/foldables)

Android isn't one size. Switch navigation by width: **`NavigationBar`** on compact (<600dp), **`NavigationRail`** on medium, rail/`NavigationDrawer` on expanded. Use `LayoutBuilder` / `MediaQuery.sizeOf(context).width` breakpoints. Don't stretch phone layouts full-width on tablets — constrain content width or go multi-pane.

## 6. Accessibility (non-negotiable)

- **Touch targets ≥ 48×48dp** — wrap small icons in `IconButton`/`InkWell` with adequate padding.
- **Contrast:** M3 `onX` roles are designed to pass contrast on their `X` background — that's another reason to use roles, not hand-picked colors.
- **Respect text scaling** — don't fix heights that clip when the user enlarges font size; test with larger `textScaleFactor`.
- Add `Semantics` labels to icon-only buttons and meaningful images; ensure `InkWell`/tap feedback exists on tappable areas.

## 7. Quality checklist before calling it done

- [ ] No hardcoded colors — everything via `ColorScheme` roles.
- [ ] No bare `TextStyle` sizes — everything via `textTheme`.
- [ ] Looks correct in **both light and dark** (test `themeMode`).
- [ ] Modern M3 components used (NavigationBar, FilledButton, …).
- [ ] Consistent 8dp spacing; content in `SafeArea`; long lists use `ListView`.
- [ ] Touch targets ≥48dp; icon buttons have semantics labels.
- [ ] `const` constructors where possible (perf + a habit that keeps widgets pure).

## Verify it visually

UI is judged by eye, so actually look — don't assume it renders right. After building, run it on an Android emulator/device (`flutter run`) and **capture a screenshot of each screen in BOTH light and dark**, then inspect them for contrast, overflow, clipping, and spacing. Concretely: toggle the theme and grab both (e.g. `flutter screenshot` / the emulator's screenshot, or drive it in an integration test). Dark mode is where hardcoded colors and low-contrast text get exposed — a screen that looks fine in light can be unreadable in dark, and you won't know without seeing it. If a design system with brand colors is involved, swap the `seed` (and consider disabling dynamic color so brand colors win). For data/charts inside the app, also load the **dataviz** skill for color/legend/axis guidance.
