import type StorageBase from "./base";

class LocalStorageAdapter implements StorageBase {
    setItem(key: string, value: string) {
      localStorage.setItem(key, JSON.stringify(value));
    }
  
    getItem(key: string) {
      const data = localStorage.getItem(key);
      return data ? JSON.parse(data) : null;
    }
  
    removeItem(key: string) {
      localStorage.removeItem(key);
    }
  
    clear(): void {
      localStorage.clear();
    }
  }

  export default LocalStorageAdapter;