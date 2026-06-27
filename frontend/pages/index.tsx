import { useRouter } from "next/router";
import { useEffect, useState } from "react";

export default function Home() {
  const router = useRouter();
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    // Wait for router to be ready before checking auth
    if (!router.isReady) return;

    // Check if user is authenticated
    const token = localStorage.getItem("authToken");
    if (token) {
      router.push("/dashboard");
    } else {
      router.push("/login");
    }
    setIsChecking(false);
  }, [router.isReady]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <p className="text-gray-500">Redirecting...</p>
    </div>
  );
}
