"use client";
import React from 'react';
import { GameState, EMPTY, PLAYER1, PLAYER2, ADJACENT_NODES, getRemovablePieces, isPartOfMill } from '@/lib/gameLogic';

const COORDS = [
  { x: 10, y: 10 }, { x: 50, y: 10 }, { x: 90, y: 10 },
  { x: 25, y: 25 }, { x: 50, y: 25 }, { x: 75, y: 25 },
  { x: 40, y: 40 }, { x: 50, y: 40 }, { x: 60, y: 40 },
  { x: 10, y: 50 }, { x: 25, y: 50 }, { x: 40, y: 50 }, { x: 60, y: 50 }, { x: 75, y: 50 }, { x: 90, y: 50 },
  { x: 40, y: 60 }, { x: 50, y: 60 }, { x: 60, y: 60 },
  { x: 25, y: 75 }, { x: 50, y: 75 }, { x: 75, y: 75 },
  { x: 10, y: 90 }, { x: 50, y: 90 }, { x: 90, y: 90 },
];

interface BoardProps {
  state: GameState;
  selectedNode: number | null;
  onNodeClick: (node: number) => void;
}

export default function Board({ state, selectedNode, onNodeClick }: BoardProps) {
  const opponent = state.turn === PLAYER1 ? PLAYER2 : PLAYER1;
  const removablePieces = state.remove_mode ? getRemovablePieces(state.board, opponent) : [];

  return (
    <div className="relative w-full max-w-2xl aspect-square mx-auto bg-neutral-900 rounded-2xl shadow-2xl p-4 sm:p-8">
      <svg width="100%" height="100%" viewBox="0 0 100 100" className="overflow-visible">
        {/* Draw lines */}
        {Object.entries(ADJACENT_NODES).map(([nodeStr, adjs]) => {
          const node = parseInt(nodeStr);
          const start = COORDS[node];
          return adjs.filter(adj => adj > node).map(adj => {
            const end = COORDS[adj];
            return (
              <line
                key={`line-${node}-${adj}`}
                x1={start.x} y1={start.y}
                x2={end.x} y2={end.y}
                stroke="#333" strokeWidth="1"
              />
            );
          });
        })}

        {/* Draw Nodes and Pieces */}
        {COORDS.map((coord, i) => {
          const piece = state.board[i];
          const isSelected = selectedNode === i;
          const isRemovable = state.remove_mode && removablePieces.includes(i);
          
          let fill = "#222";
          let stroke = "#444";
          let radius = 2;

          if (piece === PLAYER1) {
            fill = "#111"; stroke = "#555"; radius = 3.5;
          } else if (piece === PLAYER2) {
            fill = "#f5f5f5"; stroke = "#ccc"; radius = 3.5;
          }

          if (isSelected) stroke = "#3b82f6"; // Blue highlight
          if (isRemovable) stroke = "#ef4444"; // Red highlight

          return (
            <circle
              key={`node-${i}`}
              cx={coord.x} cy={coord.y}
              r={radius}
              fill={fill}
              stroke={stroke}
              strokeWidth={isSelected || isRemovable ? "0.8" : "0.3"}
              className="cursor-pointer transition-all duration-300 hover:opacity-80"
              onClick={() => onNodeClick(i)}
            >
              {isRemovable && (
                <animate attributeName="r" values="3.5;4.5;3.5" dur="1.5s" repeatCount="indefinite" />
              )}
            </circle>
          );
        })}
      </svg>
    </div>
  );
}
