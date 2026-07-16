import type { Metadata } from "next";
import { Barlow_Condensed, Manrope } from "next/font/google";
import "./globals.css";

const display = Barlow_Condensed({
  variable: "--font-display",
  subsets: ["latin"],
  weight: ["600", "700", "800", "900"],
});

const body = Manrope({
  variable: "--font-body",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://graces-takeaway.vercel.app"),
  title: "Grace’s Takeaway | Piltown, Co. Kilkenny",
  description:
    "Freshly cooked takeaway favourites from Grace’s on Main Street, Piltown. Call 051 643 759 to order.",
  openGraph: {
    title: "Grace’s Takeaway — Piltown",
    description: "Local favourites, cooked fresh. Call ahead for collection.",
    locale: "en_IE",
    type: "website",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en-IE">
      <body className={`${display.variable} ${body.variable}`}>{children}</body>
    </html>
  );
}
