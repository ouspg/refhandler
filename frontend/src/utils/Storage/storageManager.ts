import type StorageBase from "./base";
import { StorageFactory } from "./storageFactory";

export class StorageManager {
  private static instance: StorageBase;

  static init(type: "local" | "session" | "redis" = "local") {
    const storage = StorageFactory.createStorage(type);
    if(!storage) {
      throw new Error("Storage not found");
    }
    this.instance = storage;
  }

  static getInstance(): StorageBase {
    if (!this.instance) {
      throw new Error("StorageManager not initialized. Call StorageManager.init() first.");
    }
    return this.instance;
  }
}
