import React, { useRef, useEffect } from 'react';
import { FrameData } from '../types/tracking';

interface PitchRadarProps {
  frame: FrameData | null;
}

export const PitchRadar: React.FC<PitchRadarProps> = ({ frame }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Use internal logical resolution for crisp rendering
    const width = canvas.width;
    const height = canvas.height;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    // --- Draw Pitch Background ---
    ctx.fillStyle = '#051f11'; // Deep tactical green
    ctx.fillRect(0, 0, width, height);

    // --- Draw Pitch Lines (Glowing White/Emerald) ---
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.25)';
    ctx.lineWidth = 2;
    ctx.shadowColor = 'rgba(255, 255, 255, 0.4)';
    ctx.shadowBlur = 4;

    const marginX = 30;
    const marginY = 30;
    const pitchW = width - (marginX * 2);
    const pitchH = height - (marginY * 2);

    // Outer Boundary
    ctx.strokeRect(marginX, marginY, pitchW, pitchH);

    // Halfway Line
    ctx.beginPath();
    ctx.moveTo(width / 2, marginY);
    ctx.lineTo(width / 2, height - marginY);
    ctx.stroke();

    // Center Circle
    ctx.beginPath();
    ctx.arc(width / 2, height / 2, 60, 0, Math.PI * 2);
    ctx.stroke();

    // Center Dot
    ctx.beginPath();
    ctx.arc(width / 2, height / 2, 3, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
    ctx.fill();

    // Penalty Boxes (Left and Right)
    const penBoxW = pitchW * 0.16;
    const penBoxH = pitchH * 0.44;
    const penBoxY = marginY + (pitchH - penBoxH) / 2;
    ctx.strokeRect(marginX, penBoxY, penBoxW, penBoxH);
    ctx.strokeRect(width - marginX - penBoxW, penBoxY, penBoxW, penBoxH);

    // Reset shadow for entities
    ctx.shadowBlur = 0;

    // --- Draw Entities ---
    if (frame && frame.entities) {
      frame.entities.forEach((entity) => {
        // Our backend scales coordinates to 0-100 percentage
        const px = (entity.position[0] / 100) * width;
        const py = (entity.position[1] / 100) * height;

        ctx.beginPath();
        if (entity.label === 'ball') {
          // Ball: Small white glowing dot
          ctx.arc(px, py, 5, 0, Math.PI * 2);
          ctx.fillStyle = '#ffffff';
          ctx.shadowColor = '#ffffff';
          ctx.shadowBlur = 12;
        } else {
          // Player: Emerald/Cyan dot
          ctx.arc(px, py, 7, 0, Math.PI * 2);
          ctx.fillStyle = '#0ea5e9'; // Tailwind sky-500
          ctx.shadowColor = '#0ea5e9';
          ctx.shadowBlur = 8;
        }
        ctx.fill();
        ctx.closePath();

        // Draw Player ID text
        if (entity.label === 'player') {
            ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
            ctx.shadowBlur = 0;
            ctx.font = '12px "Inter", sans-serif';
            ctx.fillText(entity.id.toString(), px + 10, py - 10);
        }
      });
    }
  }, [frame]);

  return (
    <div className="w-full h-full relative rounded-xl overflow-hidden shadow-[0_0_40px_rgba(16,185,129,0.05)] border border-emerald-900/30">
      <canvas
        ref={canvasRef}
        width={1000}
        height={650}
        className="w-full h-full object-cover bg-neutral-950"
      />
    </div>
  );
};
