# CSS Classes Create
```
:root { //creates values
  --workout-cardio: #d6455d;
  --workout-strength: #2f8f5b;
  --workout-yoga: #6a5acd;
}

@theme inline { // registers the css values
  --color-workout-cardio: var(--workout-cardio);
  --color-workout-strength: var(--workout-strength);
  --color-workout-yoga: var(--workout-yoga);
}
```

Applying:
```
const typeColor = {
  cardio: "border-workout-cardio text-workout-cardio",
  strength: "border-workout-strength text-workout-strength",
  yoga: "border-workout-yoga text-workout-yoga",
};

<li className={`workout-item ${typeColor[w.type]}`}>
  {w.name}
</li>
```
- :root just creates CSS custom properties (variables) scoped globally. It's plain CSS and It's just a place to define raw values (--brand: #1f6b4a;) once, so they can be reused anywhere via var(--brand).
- @theme is the mechanism for telling Tailwind about your own values so it generates utility classes from them. If you use a name Tailwind already knows (like --color-blue-500), you are overriding that default.
If you use a new name (like --color-workout-green), you're adding a brand-new utility class family that didn't exist before (bg-workout-green, text-workout-green, etc.) — nothing is being overridden, it's net-new.

# Media Query CSS
@media (prefers-color-scheme: dark) {
  :root {
    --background: #0a0a0a;
    --foreground: #ededed;
  }
}
- prefers-color-scheme: dark is a media query that checks the user's OS/browser-level setting — whether they have dark mode turned on at the system level (macOS "Appearance: Dark," Windows dark theme, etc.). If that's true, this block runs and redefines --background and --foreground to dark-mode values, overriding whatever was set in the plain :root block earlier in the file.
Because CSS custom properties follow normal cascade rules, the later/more-specific declaration wins. So the flow is:

- :root { --background: #f4f6f4; ... } sets the default (light) values.
- @media (prefers-color-scheme: dark) { :root { --background: #0a0a0a; ... } } — if the media query matches, this overwrites those two variables with dark equivalents.
- Everything else in your CSS that uses var(--background) or var(--foreground) (like your body rule) automatically picks up whichever value won — you don't have to write separate dark-mode rules for every component.

# box-sizing
```
/* content-box (default) */
.box {
  width: 200px;
  padding: 20px;
  border: 2px solid black;
}
/* Actual rendered width = 200 + 20+20 + 2+2 = 244px */
```
```
/* border-box */
.box {
  width: 200px;
  padding: 20px;
  border: 2px solid black;
}
/* Actual rendered width = 200px, period. Content area shrinks to fit. */
```

# Page Sizing AND we can add styles to our own classes we define in react
```
html,
body {
  min-height: 100%;
}
```
- This ensures the <html> and <body> elements are at least as tall as the viewport, even if there's very little content on the page.
- Without this, if a page has just one line of text, <body> would only be as tall as that text

# Inheritence
```
CSS has two categories of properties, and each property individually is defined as one or the other by the CSS spec:

Inherited by default — text/typography-related properties, mostly:

color
font-family, font-size, font-weight
line-height
text-align
visibility
letter-spacing

Not inherited by default — layout/box-model-related properties, mostly:

background (and background-color, background-image, etc.)
border
margin, padding
width, height
display
position
```