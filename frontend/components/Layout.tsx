"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  LayoutDashboard,
  Upload,
  History,
  Settings,
  LogOut,
  BarChart3,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface LayoutProps {
  children: React.ReactNode;
  activePage?: string;
}

const Layout: React.FC<LayoutProps> = ({ children, activePage = "dashboard" }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const navItems = [
    { name: "首页", href: "/", icon: LayoutDashboard },
    { name: "上传", href: "/upload", icon: Upload },
    { name: "历史记录", href: "/history", icon: History },
    { name: "设置", href: "/settings", icon: Settings },
  ];

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      {/* Sidebar */}
      <aside
        className={cn(
          "fixed left-0 top-0 z-40 h-screen w-64 transform border-r border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-950 transition-transform duration-300 ease-in-out",
          isSidebarOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        )}
      >
        <div className="flex h-16 items-center border-b border-slate-200 px-6 dark:border-slate-800">
          <div className="flex items-center space-x-2">
            <BarChart3 className="h-8 w-8 text-blue-600" />
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              AI Sales Coach
            </h1>
          </div>
        </div>

        <nav className="flex flex-col space-y-1 px-4 py-6">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activePage === item.href.slice(1) || (activePage === "" && item.href === "/");
            return (
              <Button
                key={item.href}
                variant={isActive ? "default" : "ghost"}
                className={cn(
                  "justify-start space-x-3 rounded-lg",
                  isActive
                    ? "bg-blue-600 text-white hover:bg-blue-700"
                    : "text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white"
                )}
                asChild
              >
                <Link href={item.href}>
                  <Icon className="h-5 w-5" />
                  <span>{item.name}</span>
                </Link>
              </Button>
            );
          })}
        </nav>

        <div className="absolute bottom-6 left-4 right-4">
          <Button
            variant="ghost"
            className="w-full justify-start space-x-3 text-slate-600 hover:text-red-600 dark:text-slate-400 dark:hover:text-red-400"
            onClick={() => {
              // Logout functionality
              console.log("Logout");
            }}
          >
            <LogOut className="h-5 w-5" />
            <span>退出</span>
          </Button>
        </div>
      </aside>

      {/* Main Content */}
      <div
        className={cn(
          "flex-1 transition-all duration-300",
          isSidebarOpen ? "lg:ml-64" : "lg:ml-0"
        )}
      >
        {/* Header */}
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white/95 px-6 backdrop-blur supports-[backdrop-filter]:bg-white/60 dark:border-slate-800 dark:bg-slate-950/95">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            >
              <LayoutDashboard className="h-5 w-5" />
            </Button>
            <h2 className="text-xl font-semibold text-slate-900 dark:text-white">
              {navItems.find((item) =>
                activePage === "" && item.href === "/"
                  ? true
                  : item.href === `/${activePage}`
              )?.name || activePage}
            </h2>
          </div>

          <div className="flex items-center gap-4">
            <div className="h-8 w-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500" />
          </div>
        </header>

        {/* Page Content */}
        <main className="p-6">
          {children}
        </main>
      </div>

      {/* Mobile sidebar backdrop */}
      {!isSidebarOpen && (
        <div
          className="fixed inset-0 z-30 bg-slate-900/50 lg:hidden"
          onClick={() => setIsSidebarOpen(true)}
        />
      )}
    </div>
  );
};

export default Layout;
