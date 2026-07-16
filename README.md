# Grace’s Takeaway — Piltown

A modern, mobile-first website for Grace’s Takeaway on Main Street in Piltown, Co. Kilkenny. Built with Next.js, TypeScript and Tailwind CSS, and ready for deployment to Vercel.

## Getting started

This project uses pnpm.

```bash
pnpm install
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000).

## Useful commands

```bash
pnpm dev      # Start the local development server
pnpm lint     # Run ESLint
pnpm build    # Create a production build
pnpm start    # Run the production build
```

## Business information

- **Address:** Main Street, Banagher, Piltown, Co. Kilkenny, Ireland
- **Phone:** [051 643 759](tel:+35351643759)
- **Hours:** Wed–Thu 4:00–10:30 pm; Fri 3:00–11:00 pm; Sat–Sun 4:00–11:00 pm; Mon–Tue closed

Business details were checked against public listings in July 2026. Opening hours may vary on bank holidays and should be confirmed directly with the takeaway before future updates.

## Deployment

Push this repository to GitHub, then import it into Vercel. Vercel will detect Next.js automatically and use the standard build settings.

## Project structure

```text
app/
  globals.css   Global styles and Tailwind import
  layout.tsx    Metadata, fonts and root layout
  page.tsx      Main landing page
```

This directory is the sole Git repository. Do not initialise repositories inside subdirectories or add generated folders as submodules.
