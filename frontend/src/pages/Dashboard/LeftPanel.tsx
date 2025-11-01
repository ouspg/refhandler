import React, { useRef, useState, useEffect } from 'react';

type UploadFile = {
  id: string;
  file: File;
  progress: number;
  status: 'queued' | 'uploading' | 'done' | 'error';
};

const LeftPanel: React.FC = () => {
  const [files, setFiles] = useState<UploadFile[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const intervals = useRef<Record<string, number>>({});

  useEffect(() => {
    return () => {
      // clear any running intervals on unmount
      Object.values(intervals.current).forEach((id) => clearInterval(id));
    };
  }, []);

  const addFiles = (selected: FileList | null) => {
    if (!selected) return;
    const newItems: UploadFile[] = Array.from(selected).map((f) => ({
      id: `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`,
      file: f,
      progress: 0,
      status: 'queued',
    }));

    setFiles((prev) => {
      const combined = [...prev, ...newItems];
      // start uploading newly added files
      newItems.forEach(startUpload);
      return combined;
    });
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    addFiles(e.target.files);
    // reset input so same file can be selected again if needed
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const startUpload = (item: UploadFile) => {
    setFiles((prev) =>
      prev.map((p) => (p.id === item.id ? { ...p, status: 'uploading' } : p))
    );

    // simulate upload progress
    const id = window.setInterval(() => {
      setFiles((prev) =>
        prev.map((p) => {
          if (p.id !== item.id) return p;
          const next = Math.min(
            100,
            p.progress + Math.floor(Math.random() * 20) + 5
          );
          if (next >= 100) {
            clearInterval(intervals.current[item.id]);
            delete intervals.current[item.id];
            return { ...p, progress: 100, status: 'done' };
          }
          return { ...p, progress: next };
        })
      );
    }, 300);

    intervals.current[item.id] = id;
  };

  const removeFile = (id: string) => {
    if (intervals.current[id]) {
      clearInterval(intervals.current[id]);
      delete intervals.current[id];
    }
    setFiles((prev) => prev.filter((f) => f.id !== id));
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      // Placeholder behaviour: in real app you'd send files or references to backend
      const completed = files.filter((f) => f.status === 'done');
      console.log(
        'Submitting files',
        completed.map((f) => f.file.name)
      );
      // Simulate network delay
      await new Promise((r) => setTimeout(r, 700));
      // You can update UI to show final submission state here
      alert(`Submitted ${completed.length} files`);
    } catch (err) {
      console.error(err);
      alert('Submission failed');
    } finally {
      setSubmitting(false);
    }
  };

  const allDone = files.length > 0 && files.every((f) => f.status === 'done');

  return (
    <div className="dashboard-left">
      <h2>Attachments</h2>

      <div className="upload-area">
        <input
          ref={fileInputRef}
          id="file-input"
          type="file"
          multiple
          onChange={handleFileInput}
          style={{ display: 'none' }}
        />
        <div className="upload-controls">
          <label htmlFor="file-input" className="choose-button">
            Choose files
          </label>
          <button
            type="button"
            className="clear-button"
            onClick={() => setFiles([])}
            disabled={files.length === 0}
          >
            Clear
          </button>
        </div>
        <p className="hint">
          You can add multiple files. Upload will start automatically.
        </p>
      </div>

      <div className="file-list">
        {files.map((f) => (
          <div className="file-item" key={f.id}>
            <div className="file-meta">
              <strong className="file-name">{f.file.name}</strong>
              <span className="file-size">
                {(f.file.size / 1024).toFixed(1)} KB
              </span>
            </div>

            <div className="progress">
              <div
                className="progress-bar"
                style={{ width: `${f.progress}%` }}
              />
            </div>

            <div className="file-actions">
              <span className="status">{f.status}</span>
              <button
                className="remove-button"
                onClick={() => removeFile(f.id)}
              >
                Remove
              </button>
            </div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: 12 }}>
        <button
          className="submit-button"
          onClick={handleSubmit}
          disabled={!allDone || submitting}
        >
          {submitting ? 'Submitting...' : 'Submit attachments'}
        </button>
      </div>
    </div>
  );
};

export default LeftPanel;
