import LocalStorageAdapter from "./localStorage";

export class StorageFactory {
  static createStorage(type: "local" | "session" | "redis" | null = "local") {
    switch (type) {
      case "local":
        return new LocalStorageAdapter();
    }
  }
}