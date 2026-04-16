# Prof. Ts. Dr.-Ing. Lau Sian Lun — Personal Website

A modern, responsive personal website for Prof. Ts. Dr.-Ing. Lau Sian Lun — Researcher, Educator, and IEEE Senior Member at Sunway University.

## Features

- Modern tech aesthetic with clean card-based layout
- Dark/light mode with system preference detection
- Scroll animations and animated stat counters
- Fully responsive design (mobile, tablet, desktop)
- Sections: About, Research, Publications, Projects, Teaching, Professional Activities, Blog, Contact
- No build tools required — pure HTML, CSS, and JavaScript

## Structure

```
.
├── index.html                # Single-page site
├── assets/
│   ├── css/style.css         # Modern CSS with CSS variables and dark mode
│   ├── js/main.js            # Theme toggle, animations, counter, scroll effects
│   └── img/avatar.svg        # Placeholder avatar — replace with a real photo
├── .nojekyll                 # Bypasses Jekyll processing on GitHub Pages
└── README.md
```

## Customization

- **Avatar**: Replace `assets/img/avatar.svg` with your photo (e.g., `avatar.jpg`) and update the `<img src=...>` in the hero section
- **Social links**: Update GitHub, LinkedIn, ResearchGate URLs to your actual profiles
- **Publications**: Add more publications as they are published
- **Blog posts**: Update with your latest WordPress posts
- **Colors**: Modify CSS variables in `:root` block in `style.css`

## Deploy to GitHub Pages

1. Push to the repo `sianlun.github.io`
2. Go to Settings > Pages > Source > Deploy from branch > `main` / `/ (root)`
3. Your site will be live at `https://sianlun.github.io`

## License

Content © Lau Sian Lun. Template code free to reuse.
