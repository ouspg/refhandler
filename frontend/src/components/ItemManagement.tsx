import React from 'react';

type Item = {
  id: number;
  title: string;
  description: string;
};

const sampleItems: Item[] = [
  { id: 1, title: 'Item #1', description: 'Item description' },
  { id: 2, title: 'Item #2', description: 'Item description' },
  { id: 3, title: 'Item #3', description: 'Item description' },
  { id: 4, title: 'Item #4', description: 'Item description' },
  { id: 5, title: 'Item #5', description: 'Item description' },
  { id: 6, title: 'Item #6', description: 'Item description' },
  { id: 7, title: 'Item #7', description: 'Item description' },
  { id: 8, title: 'Item #8', description: 'Item description' },
];

type ItemManagementProps = {
  pageName: string;
  onAdd: () => void;
};

const ItemManagement: React.FC<ItemManagementProps> = ({ pageName, onAdd }) => {
  const items = sampleItems;

  return (
    <div style={styles.page}>
      <div style={styles.headerRow}>
        <h2 style={styles.title}>{pageName} Management</h2>
        <button style={styles.addButton} aria-label="Add Item" onClick={onAdd}>
          + Add {pageName}
        </button>
      </div>

      <div style={styles.card}>
        <table style={styles.table}>
          <thead style={styles.thead}>
            <tr>
              <th style={{ ...styles.th, ...styles.idCell }}>ID</th>
              <th style={styles.th}>Title</th>
              <th style={styles.th}>Description</th>
              <th style={{ ...styles.th, ...styles.actionsCell }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {items.length === 0 && (
              <tr>
                <td style={styles.emptyRow} colSpan={4}>
                  No items found
                </td>
              </tr>
            )}

            {items.map((it) => (
              <tr key={it.id} style={styles.tr}>
                <td style={{ ...styles.td, ...styles.idCell }}>{it.id}</td>
                <td style={styles.td}>{it.title}</td>
                <td style={styles.td}>{it.description}</td>
                <td style={{ ...styles.td, ...styles.actionsCell }}>
                  <button
                    aria-label={`Actions for ${it.title}`}
                    title="Actions"
                    style={styles.kebab}
                  >
                    ⋮
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ItemManagement;

const styles: { [key: string]: React.CSSProperties } = {
  page: {
    padding: '28px',
    fontFamily:
      "Inter, Roboto, -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, 'Helvetica Neue', Arial",
    color: '#2d3748',
    /* match global soft background instead of pure white */
    background: '#f4f7fb',
    minHeight: '100%',
  },
  headerRow: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: '20px',
  },
  title: {
    fontSize: '20px',
    fontWeight: 600,
    margin: 0,
  },
  addButton: {
    backgroundColor: '#0ea5a4', // teal-500
    color: '#fff',
    border: 'none',
    padding: '8px 14px',
    borderRadius: '6px',
    cursor: 'pointer',
    boxShadow: '0 1px 2px rgba(16,24,40,0.05)',
    fontWeight: 600,
  },
  card: {
    borderTop: '1px solid #e6eef0',
    paddingTop: '8px',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    marginTop: '8px',
  },
  thead: {
    textAlign: 'left',
    fontSize: '12px',
    color: '#64748b',
    textTransform: 'uppercase',
    letterSpacing: '0.06em',
    borderBottom: '1px solid #e6eef0',
  },
  th: {
    padding: '14px 12px',
    fontWeight: 700,
  },
  tr: {
    borderBottom: '1px solid #f1f5f9',
  },
  td: {
    padding: '18px 12px',
    verticalAlign: 'middle',
    color: '#344054',
  },
  idCell: {
    width: '60px',
    color: '#94a3b8',
  },
  actionsCell: {
    width: '70px',
    textAlign: 'right',
  },
  kebab: {
    background: 'transparent',
    border: 'none',
    cursor: 'pointer',
    fontSize: '18px',
    color: '#94a3b8',
    padding: '4px 8px',
  },
  emptyRow: {
    padding: '30px 12px',
    color: '#64748b',
    textAlign: 'center',
  },
};
