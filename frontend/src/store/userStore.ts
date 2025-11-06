import { create } from 'zustand';

interface UserState {
  user: boolean;
  setUser: (user: boolean) => void;
}

export const useUserStore = create<UserState>((set) => ({
  user: false,
  setUser: (user) => set({ user }),
}));
