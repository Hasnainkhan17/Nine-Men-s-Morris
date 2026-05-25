export const EMPTY = 0;
export const PLAYER1 = 1;
export const PLAYER2 = 2;
export const PHASE_PLACING = 1;
export const PHASE_MOVING_FLYING = 2;

export const ADJACENT_NODES: Record<number, number[]> = {
  0: [1, 9], 1: [0, 2, 4], 2: [1, 14], 3: [4, 10], 4: [1, 3, 5, 7], 5: [4, 13],
  6: [7, 11], 7: [4, 6, 8], 8: [7, 12], 9: [0, 10, 21], 10: [3, 9, 11, 18],
  11: [6, 10, 15], 12: [8, 13, 17], 13: [5, 12, 14, 20], 14: [2, 13, 23],
  15: [11, 16], 16: [15, 17, 19], 17: [12, 16], 18: [10, 19], 19: [16, 18, 20, 22],
  20: [13, 19], 21: [9, 22], 22: [19, 21, 23], 23: [14, 22]
};

export const MILLS: number[][] = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14],
  [15, 16, 17], [18, 19, 20], [21, 22, 23], [0, 9, 21], [3, 10, 18],
  [6, 11, 15], [1, 4, 7], [16, 19, 22], [8, 12, 17], [5, 13, 20], [2, 14, 23]
];

export interface GameState {
  board: number[];
  turn: number;
  unplaced_pieces: { [key: string]: number };
  phase: number;
  remove_mode: boolean;
  game_over: boolean;
  winner: number | null;
}

export const getInitialState = (): GameState => ({
  board: Array(24).fill(EMPTY),
  turn: PLAYER1,
  unplaced_pieces: { "1": 9, "2": 9 },
  phase: PHASE_PLACING,
  remove_mode: false,
  game_over: false,
  winner: null
});

export const formsMill = (board: number[], node: number, player: number): boolean => {
  for (const mill of MILLS) {
    if (mill.includes(node)) {
      if (mill.every(n => board[n] === player || n === node)) {
        return true;
      }
    }
  }
  return false;
};

export const isPartOfMill = (board: number[], node: number, player: number): boolean => {
  if (board[node] !== player) return false;
  for (const mill of MILLS) {
    if (mill.includes(node)) {
      if (mill.every(n => board[n] === player)) {
        return true;
      }
    }
  }
  return false;
};

export const getRemovablePieces = (board: number[], player: number): number[] => {
  const pieces = board.map((p, i) => (p === player ? i : -1)).filter(i => i !== -1);
  const nonMill = pieces.filter(p => !isPartOfMill(board, p, player));
  return nonMill.length > 0 ? nonMill : pieces;
};

export const checkGameOver = (state: GameState): GameState => {
  if (state.phase === PHASE_PLACING) return state;
  const p1 = state.board.filter(p => p === PLAYER1).length;
  const p2 = state.board.filter(p => p === PLAYER2).length;
  
  if (p1 < 3) return { ...state, game_over: true, winner: PLAYER2 };
  if (p2 < 3) return { ...state, game_over: true, winner: PLAYER1 };
  
  const currPieces = state.board.map((p, i) => (p === state.turn ? i : -1)).filter(i => i !== -1);
  if (currPieces.length > 3) {
    const hasMoves = currPieces.some(node => 
      ADJACENT_NODES[node].some(adj => state.board[adj] === EMPTY)
    );
    if (!hasMoves) {
      return { ...state, game_over: true, winner: state.turn === PLAYER1 ? PLAYER2 : PLAYER1 };
    }
  }
  
  return state;
};

export const switchTurn = (state: GameState): GameState => {
  const nextTurn = state.turn === PLAYER1 ? PLAYER2 : PLAYER1;
  const nextPhase = (state.unplaced_pieces["1"] === 0 && state.unplaced_pieces["2"] === 0) 
    ? PHASE_MOVING_FLYING 
    : state.phase;
    
  return checkGameOver({
    ...state,
    turn: nextTurn,
    phase: nextPhase
  });
};

export const handleNodeClick = (state: GameState, node: number, selectedNode: number | null): { newState: GameState, newSelected: number | null } => {
  if (state.game_over) return { newState: state, newSelected: selectedNode };
  
  let nextState = { ...state, board: [...state.board], unplaced_pieces: { ...state.unplaced_pieces } };
  
  if (state.remove_mode) {
    const opponent = state.turn === PLAYER1 ? PLAYER2 : PLAYER1;
    if (state.board[node] === opponent) {
      const removable = getRemovablePieces(state.board, opponent);
      if (removable.includes(node)) {
        nextState.board[node] = EMPTY;
        nextState.remove_mode = false;
        nextState = switchTurn(nextState);
      }
    }
    return { newState: nextState, newSelected: null };
  }
  
  if (state.phase === PHASE_PLACING) {
    if (state.board[node] === EMPTY) {
      nextState.board[node] = state.turn;
      nextState.unplaced_pieces[state.turn.toString()] -= 1;
      
      if (formsMill(nextState.board, node, state.turn)) {
        nextState.remove_mode = true;
      } else {
        nextState = switchTurn(nextState);
      }
    }
    return { newState: nextState, newSelected: null };
  }
  
  if (state.phase === PHASE_MOVING_FLYING) {
    if (state.board[node] === state.turn) {
      return { newState: state, newSelected: node };
    }
    
    if (selectedNode !== null && state.board[node] === EMPTY) {
      const piecesCount = state.board.filter(p => p === state.turn).length;
      const isFlying = piecesCount === 3;
      
      if (isFlying || ADJACENT_NODES[selectedNode].includes(node)) {
        nextState.board[node] = state.turn;
        nextState.board[selectedNode] = EMPTY;
        
        if (formsMill(nextState.board, node, state.turn)) {
          nextState.remove_mode = true;
        } else {
          nextState = switchTurn(nextState);
        }
        return { newState: nextState, newSelected: null };
      }
    }
  }
  
  return { newState: state, newSelected: selectedNode };
};
