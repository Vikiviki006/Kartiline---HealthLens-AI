import React, { useState, useEffect, useRef } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import { Layout } from "@/components/Layout";
import { useReports, ReportDetail } from "@/lib/hooks/useReports";
import { Send, Loader, MessageCircle, ArrowLeft, Bot, User, Sparkles } from "lucide-react";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export default function ChatPage() {
  const router = useRouter();
  const { id } = router.query;
  const [report, setReport] = useState<ReportDetail | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const { getReport } = useReports();
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!id) return;

    const fetchReport = async () => {
      const data = await getReport(id as string);
      setReport(data);
      setLoading(false);

      // Add welcome message
      setMessages([
        {
          id: "1",
          role: "assistant",
          content: `Welcome to the HealthLens AI Chat! I'm here to help you understand your medical report. Feel free to ask any questions about your markers, values, or health status. What would you like to know?`,
          timestamp: new Date(),
        },
      ]);
    };

    fetchReport();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || !id) return;

    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setSending(true);

    try {
      const response = await import("@/lib/api").then(m => m.default.post(`/reports/${id}/chat`, { question: userMessage.content }));
      
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content:
          response.data.answer ||
          response.data.data?.answer ||
          response.data.message ||
          "Sorry, I couldn't process your request.",
          timestamp: new Date(),
        };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "I'm sorry, there was an error processing your request. Please try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setSending(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center items-center h-[80vh]">
          <div className="relative w-16 h-16">
            <div className="absolute inset-0 rounded-full border-t-2 border-indigo-500 animate-spin"></div>
            <div className="absolute inset-2 rounded-full border-t-2 border-cyan-400 animate-spin" style={{ animationDirection: 'reverse' }}></div>
            <Sparkles className="absolute inset-0 m-auto w-6 h-6 text-indigo-500 animate-pulse" />
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="h-[calc(100vh-6rem)] -mt-4 -mx-4 px-4 pb-4 flex flex-col bg-gradient-to-br from-indigo-50/50 via-white to-cyan-50/50">
        {/* Header */}
        <div className="mb-4 flex flex-col md:flex-row justify-between items-start md:items-center p-6 bg-white/40 backdrop-blur-xl rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-white/60">
          <div>
            <Link href={`/report/${id}`} className="inline-flex items-center gap-2 text-indigo-600 hover:text-indigo-800 transition-colors text-sm font-semibold mb-3 bg-indigo-50/50 px-3 py-1.5 rounded-full">
              <ArrowLeft className="w-4 h-4" /> Back to Report
            </Link>
            <h1 className="text-2xl md:text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-700 to-cyan-600 flex items-center gap-3">
              <MessageCircle className="w-8 h-8 text-indigo-600" />
              HealthLens AI Assistant
            </h1>
            {report && (
              <p className="text-slate-500 mt-2 text-sm font-medium flex items-center gap-2">
                <span className="relative flex h-2.5 w-2.5">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                </span>
                Analyzing context from: <span className="text-indigo-900 font-semibold">{report.original_filename}</span>
              </p>
            )}
          </div>
        </div>

        {/* Chat Container */}
        <div className="flex-1 bg-white/60 backdrop-blur-2xl border border-white/80 rounded-3xl overflow-hidden flex flex-col shadow-[0_8px_30px_rgb(0,0,0,0.08)]">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"} animate-in fade-in slide-in-from-bottom-4 duration-300`}
              >
                <div className={`flex gap-3 max-w-[85%] md:max-w-[75%] ${msg.role === "user" ? "flex-row-reverse" : "flex-row"}`}>
                  <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center shadow-sm ${
                    msg.role === "user" ? "bg-indigo-600 text-white" : "bg-gradient-to-br from-cyan-500 to-blue-600 text-white"
                  }`}>
                    {msg.role === "user" ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
                  </div>
                  
                  <div
                    className={`px-5 py-4 rounded-2xl shadow-sm ${
                      msg.role === "user"
                        ? "bg-indigo-600 text-white rounded-tr-sm"
                        : "bg-white text-slate-800 rounded-tl-sm border border-slate-100"
                    }`}
                  >
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                    <p
                      className={`text-[10px] mt-2 font-medium tracking-wide ${
                        msg.role === "user" ? "text-indigo-200" : "text-slate-400"
                      }`}
                    >
                      {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                </div>
              </div>
            ))}
            {sending && (
              <div className="flex justify-start animate-in fade-in duration-300">
                <div className="flex gap-3 max-w-[85%] flex-row">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-cyan-500 to-blue-600 text-white flex items-center justify-center shadow-sm">
                    <Bot className="w-5 h-5" />
                  </div>
                  <div className="bg-white px-5 py-4 rounded-2xl rounded-tl-sm border border-slate-100 shadow-sm flex items-center gap-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                      <div className="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                      <div className="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={endOfMessagesRef} />
          </div>

          {/* Input */}
          <form onSubmit={handleSendMessage} className="bg-white/80 border-t border-slate-100 p-4 md:p-6 backdrop-blur-md">
            <div className="flex space-x-3 max-w-4xl mx-auto">
              <div className="relative flex-1">
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Ask about your health markers, advice, or summary..."
                  className="w-full pl-5 pr-12 py-4 bg-slate-50/50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all shadow-sm text-slate-800 placeholder:text-slate-400"
                  disabled={sending}
                />
              </div>
              <button
                type="submit"
                disabled={sending || !inputValue.trim()}
                className="px-6 py-4 bg-gradient-to-r from-indigo-600 to-cyan-600 text-white rounded-2xl hover:shadow-lg hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:hover:shadow-none disabled:hover:translate-y-0 flex items-center justify-center min-w-[3.5rem]"
              >
                {sending ? <Loader className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
              </button>
            </div>
            <p className="text-center text-xs text-slate-400 mt-3 font-medium">
              HealthLens AI can make mistakes. Consider verifying critical medical information with your doctor.
            </p>
          </form>
        </div>
      </div>
    </Layout>
  );
}
