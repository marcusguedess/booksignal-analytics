import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";
const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: "BookSignal Analytics",
  description:
    "Ferramenta de decisão editorial para priorizar, auditar e comparar livros a partir de CSVs ou bases autorizadas.",
  icons: {
    icon: `${basePath}/icon.svg`,
  },
  openGraph: {
    type: "website",
    title: "BookSignal Analytics",
    description:
      "Ferramenta de decisão editorial para priorizar, auditar e comparar livros a partir de CSVs ou bases autorizadas.",
    images: [`${basePath}/opengraph-image.svg`],
  },
  twitter: {
    card: "summary_large_image",
    title: "BookSignal Analytics",
    description:
      "Ferramenta de decisão editorial para priorizar, auditar e comparar livros a partir de CSVs ou bases autorizadas.",
    images: [`${basePath}/opengraph-image.svg`],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="pt-BR"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
