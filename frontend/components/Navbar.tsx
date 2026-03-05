"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export function Navbar() {
  const pathname = usePathname();

  const navItems = [
    { href: "/", label: "首页" },
    { href: "/upload", label: "上传" },
    { href: "/history", label: "历史记录" },
    { href: "/settings", label: "设置" },
  ];

  return (
    <nav className="bg-card border-b sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="text-2xl">💼</div>
            <span className="font-bold text-xl text-foreground">
              AI Sales Coaching
            </span>
          </Link>

          {/* 导航菜单 */}
          <div className="flex items-center space-x-8">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`text-sm font-medium transition-colors ${
                  pathname === item.href
                    ? "text-primary"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
}