"use client";

import React from "react";

interface RadarChartProps {
  data: Array<{
    label: string;
    value: number;
  }>;
  size?: number;
}

export function RadarChart({ data, size = 400 }: RadarChartProps) {
  const maxValue = 100;
  const angleStep = (2 * Math.PI) / data.length;
  const radius = size / 2;
  const centerX = size / 2;
  const centerY = size / 2;

  // 计算雷达图顶点坐标
  const vertices = data.map((_, i) => {
    const angle = i * angleStep - Math.PI / 2;
    return {
      x: centerX + radius * Math.cos(angle),
      y: centerY + radius * Math.sin(angle),
    };
  });

  // 计算数据点坐标
  const dataPoints = data.map((item, i) => {
    const angle = i * angleStep - Math.PI / 2;
    const pointRadius = (item.value / maxValue) * radius;
    return {
      x: centerX + pointRadius * Math.cos(angle),
      y: centerY + pointRadius * Math.sin(angle),
    };
  });

  // 绘制雷达图多边形
  const radarPath = dataPoints
    .map((point, i) => `${i === 0 ? "M" : "L"} ${point.x} ${point.y}`)
    .join(" ") + " Z";

  return (
    <div className="w-full flex justify-center">
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        className="overflow-visible"
      >
        {/* 雷达图背景网格 */}
        {[0.25, 0.5, 0.75, 1].map((level) => {
          const levelRadius = level * radius;
          const gridPath = vertices
            .map((vertex, i) => {
              const angle = i * angleStep - Math.PI / 2;
              return `${i === 0 ? "M" : "L"} ${
                centerX + levelRadius * Math.cos(angle)
              } ${centerY + levelRadius * Math.sin(angle)}`;
            })
            .join(" ") + " Z";
          
          return (
            <path
              key={level}
              d={gridPath}
              fill="none"
              stroke="currentColor"
              strokeWidth="1"
              className="text-muted-foreground/30"
            />
          );
        })}

        {/* 雷达图连线 */}
        {vertices.map((vertex, i) => (
          <line
            key={i}
            x1={centerX}
            y1={centerY}
            x2={vertex.x}
            y2={vertex.y}
            stroke="currentColor"
            strokeWidth="1"
            className="text-muted-foreground/50"
          />
        ))}

        {/* 数据多边形 */}
        <path
          d={radarPath}
          fill="currentColor"
          fillOpacity="0.3"
          stroke="currentColor"
          strokeWidth="2"
          className="text-primary"
        />

        {/* 数据点 */}
        {dataPoints.map((point, i) => (
          <circle
            key={i}
            cx={point.x}
            cy={point.y}
            r="4"
            fill="currentColor"
            className="text-primary"
          />
        ))}

        {/* 标签 */}
        {data.map((item, i) => {
          const angle = i * angleStep - Math.PI / 2;
          const labelRadius = radius * 1.15;
          const x = centerX + labelRadius * Math.cos(angle);
          const y = centerY + labelRadius * Math.sin(angle);

          return (
            <g key={i} transform={`translate(${x}, ${y})`}>
              <text
                textAnchor="middle"
                dominantBaseline="middle"
                fontSize="12"
                className="text-foreground font-medium"
              >
                {item.label}
              </text>
              <text
                textAnchor="middle"
                dominantBaseline="middle"
                fontSize="10"
                y="16"
                className="text-primary font-bold"
              >
                {item.value.toFixed(0)}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}