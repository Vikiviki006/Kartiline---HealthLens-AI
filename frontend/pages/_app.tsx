import "@/globals.css";
import type { AppProps } from "next/app";
import { useEffect } from "react";
import { useRouter } from "next/router";

export default function App({ Component, pageProps }: AppProps) {
  const router = useRouter();

  useEffect(() => {
    // Redirect to login if not authenticated
    const token = localStorage.getItem("authToken");
    const publicPages = ["/login", "/register"];
    
    if (!token && !publicPages.includes(router.pathname)) {
      router.push("/login");
    }
  }, [router]);

  return <Component {...pageProps} />;
}
