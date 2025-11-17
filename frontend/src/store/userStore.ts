import { create } from 'zustand';

export interface User {
  username: string;
  token: string;
  role?: string | undefined;
}

interface UserState {
  user: User | null;
  setUser: (user: User | null) => void;
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
}));
