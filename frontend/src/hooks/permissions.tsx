import { useEffect, useState } from "react";
import { StorageManager } from "../utils/Storage/StorageManager";

export const usePermissions = () => {
  StorageManager.init("local");
  const [permissions, setPermissions] = useState<string[]>([]);

  useEffect(() => {
    const storage = StorageManager.getInstance();
    const stored = storage.getItem("permissions");
    if (stored) {
      setPermissions(JSON.parse(stored));
    }
  }, []);

  const hasPermission = (permission: string) => {
    return permissions.includes(permission);
  };

  const hasPermissions = (required: string[]) => {
    return required.every((p) => permissions.includes(p));
  };

  const setNewPermissions = (newPermissions: string[]) => {
    setPermissions(newPermissions);
    const storage = StorageManager.getInstance();
    storage.setItem("permissions", JSON.stringify(newPermissions));
  };

  return { permissions, hasPermission, hasPermissions, setNewPermissions };
};
