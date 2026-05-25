"use client";
import React, { useState, useEffect } from 'react';
import Board from '@/components/Board';
import InstructionsModal from '@/components/InstructionsModal';
import { GameState, getInitialState, handleNodeClick, PLAYER1, PLAYER2, PHASE_PLACING } from '@/lib/gameLogic';

export default function Home() {
  const [inMenu, setInMenu] = useState(true);
  const [showInstructions, setShowInstructions] = useState(false);
  
  const [state, setState] = useState<GameState>(getInitialState());
  const [selectedNode, setSelectedNode] = useState<number | null>(null);
  
  const [isAiMode, setIsAiMode] = useState(false);
  const [aiDifficulty, setAiDifficulty] = useState('medium');
  const [isAiThinking, setIsAiThinking] = useState(false);

  // Trigger AI move if it's AI's turn
  useEffect(() => {
    if (!inMenu && isAiMode && !state.game_over && state.turn === PLAYER2) {
      const fetchAiMove = async () => {
        setIsAiThinking(true);
        try {
          const res = await fetch('/api/ai-move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ state, difficulty: aiDifficulty })
          });
          const data = await res.json();
          if (data.state) {
            setState(data.state);
            setSelectedNode(null);
          }
        } catch (error) {
          console.error("AI Move failed", error);
        } finally {
          setIsAiThinking(false);
        }
      };
      
      // Slight delay for UX
      const timer = setTimeout(() => {
        fetchAiMove();
      }, 500);
      return () => clearTimeout(timer);
    }
  }, [state.turn, inMenu, isAiMode, state.game_over, state, aiDifficulty]);

  const onNodeClick = (node: number) => {
    if (isAiThinking || (isAiMode && state.turn === PLAYER2)) return;
    
    const { newState, newSelected } = handleNodeClick(state, node, selectedNode);
    setState(newState);
    setSelectedNode(newSelected);
  };

  const startGame = (ai: boolean, diff = 'medium') => {
    setState(getInitialState());
    setSelectedNode(null);
    setIsAiMode(ai);
    setAiDifficulty(diff);
    setInMenu(false);
  };

  const forfeitGame = () => {
    setInMenu(true);
  };

  // UI Helpers
  const getMessage = () => {
    if (state.game_over) return `Game Over! Player ${state.winner} Wins!`;
    const player = state.turn === PLAYER1 ? "Player 1 (Black)" : "Player 2 (White)";
    if (state.remove_mode) return `${player} formed a Mill! Remove opponent piece.`;
    if (state.phase === PHASE_PLACING) return `${player} Placing (P1: ${state.unplaced_pieces["1"]} | P2: ${state.unplaced_pieces["2"]})`;
    return `${player} Moving`;
  };

  return (
    <main className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-4 sm:p-8 font-sans relative">
      {inMenu && (
        <div className="absolute bottom-6 right-6 text-right text-neutral-500 text-sm animate-fade-in">
          <p>Developed by:</p>
          <p className="font-medium text-neutral-400">Muhammad Hasnain</p>
          <p className="font-medium text-neutral-400">Sundas Gulzar</p>
        </div>
      )}
      {inMenu ? (
        <div className="max-w-md w-full bg-neutral-900 border border-neutral-800 p-8 rounded-3xl shadow-2xl text-center">
          <h1 className="text-4xl font-black bg-gradient-to-br from-blue-400 to-emerald-400 bg-clip-text text-transparent mb-8">
            Nine Men's Morris
          </h1>
          
          <div className="space-y-4">
            <button onClick={() => startGame(false)} className="w-full py-4 bg-neutral-800 hover:bg-neutral-700 rounded-xl font-medium transition-all">
              Play vs Human
            </button>
            <button onClick={() => startGame(true, 'easy')} className="w-full py-4 bg-neutral-800 hover:bg-neutral-700 rounded-xl font-medium transition-all">
              Play vs AI (Easy)
            </button>
            <button onClick={() => startGame(true, 'medium')} className="w-full py-4 bg-blue-900/40 hover:bg-blue-800/60 text-blue-300 border border-blue-800/50 rounded-xl font-medium transition-all">
              Play vs AI (Medium)
            </button>
            <button onClick={() => startGame(true, 'hard')} className="w-full py-4 bg-neutral-800 hover:bg-neutral-700 rounded-xl font-medium transition-all">
              Play vs AI (Hard)
            </button>
            <div className="pt-4 mt-4 border-t border-neutral-800">
              <button onClick={() => setShowInstructions(true)} className="w-full py-3 text-neutral-400 hover:text-white transition-colors">
                How to Play
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className="w-full max-w-4xl flex flex-col items-center">
          {/* Header */}
          <div className="w-full flex justify-between items-center mb-8 px-4">
            <div className="text-lg font-medium text-neutral-300">
              {getMessage()}
              {isAiThinking && <span className="ml-2 animate-pulse text-blue-400">AI is thinking...</span>}
            </div>
            <button 
              onClick={forfeitGame}
              className="px-6 py-2 bg-red-900/30 text-red-400 hover:bg-red-900/50 border border-red-900/50 rounded-lg transition-all text-sm font-medium"
            >
              Forfeit Game
            </button>
          </div>
          
          <Board state={state} selectedNode={selectedNode} onNodeClick={onNodeClick} />
          
          {state.game_over && (
            <div className="mt-8 animate-fade-in-up">
              <button onClick={forfeitGame} className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold shadow-lg shadow-blue-900/20 transition-all">
                Return to Menu
              </button>
            </div>
          )}
        </div>
      )}

      {showInstructions && <InstructionsModal onClose={() => setShowInstructions(false)} />}
    </main>
  );
}
