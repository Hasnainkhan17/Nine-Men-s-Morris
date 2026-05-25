"use client";
import React from 'react';

export default function InstructionsModal({ onClose }: { onClose: () => void }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div className="bg-neutral-900 border border-neutral-700 p-8 rounded-2xl max-w-lg w-full shadow-2xl relative">
        <h2 className="text-2xl font-bold text-white mb-4">How to Play Nine Men's Morris</h2>
        
        <div className="space-y-4 text-neutral-300 text-sm">
          <div>
            <h3 className="font-semibold text-white">Phase 1: Placing</h3>
            <p>Players take turns placing pieces onto empty spots. If you place 3 pieces in a straight line (a "Mill"), you must remove one of your opponent's pieces.</p>
          </div>
          
          <div>
            <h3 className="font-semibold text-white">Phase 2: Moving</h3>
            <p>Once all 9 pieces are placed, you can move a piece to any adjacent connected empty spot. Forming a mill again lets you remove another opponent piece.</p>
          </div>

          <div>
            <h3 className="font-semibold text-white">Phase 3: Flying</h3>
            <p>When you have only 3 pieces left, you can move them to ANY empty spot on the board, not just adjacent ones.</p>
          </div>
          
          <div>
            <h3 className="font-semibold text-white">Winning</h3>
            <p>You win if your opponent is reduced to 2 pieces, or if they have no valid moves left.</p>
          </div>
        </div>
        
        <button 
          onClick={onClose}
          className="mt-8 w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl transition-colors"
        >
          Got it!
        </button>
      </div>
    </div>
  );
}
