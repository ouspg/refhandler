import React, { useEffect } from "react";

type ModalProps = {
  title: string;
  children: React.ReactNode;
  onClose: () => void;
};

const Modal: React.FC<ModalProps> = ({ title, children, onClose }) => {

  useEffect(() => {
    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    return () => {
      document.body.style.overflow = originalOverflow;
    };
  }, []);

  return (
    <div style={styles.overlay} onClick={onClose}>
      <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div style={styles.header}>
          <h3 style={{ margin: 0 }}>{title}</h3>
          <button style={styles.closeBtn} onClick={onClose}>✕</button>
        </div>

        <div style={styles.content}>{children}</div>
      </div>
    </div>
  );
};

export default Modal;

const styles: { [key: string]: React.CSSProperties } = {
  overlay: {
    position: "fixed",
    inset: 0,
    backgroundColor: "rgba(0,0,0,0.4)",
    backdropFilter: "blur(2px)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 1000,
    animation: "fadeIn 0.15s ease",
    padding: "20px",
  },
  modal: {
    background: "#fff",
    width: "100%",
    maxWidth: "460px",
    maxHeight: "85vh",
    overflowY: "auto", // content scrolls, not background
    borderRadius: "12px",
    boxShadow: "0 4px 22px rgba(0,0,0,0.2)",
    padding: "22px",
    animation: "zoomIn 0.2s ease",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "14px",
    borderBottom: "1px solid #eee",
    paddingBottom: "10px",
  },
  closeBtn: {
    background: "transparent",
    border: "none",
    fontSize: "22px",
    cursor: "pointer",
    color: "#333",
    padding: "4px",
  },
  content: {
    marginTop: "10px",
    display: "flex",
    flexDirection: "column",
    gap: "14px",
  },
};
