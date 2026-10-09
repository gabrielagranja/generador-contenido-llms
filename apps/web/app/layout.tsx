import type { Metadata } from "next";
import "../styles/tokens.css";

export const metadata: Metadata = {
  title: "Estudio · Generador de contenido",
  description: "Espacio de trabajo editorial multimarca asistido por LLM",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
