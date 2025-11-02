import React, { useRef, useState, useEffect } from 'react';
import axios from 'axios';

type UploadFile = {
  id: string;
  file: File;
  progress: number;
  status: 'queued' | 'uploading' | 'done' | 'submitting' | 'uploaded' | 'error';
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
      // start client-side simulated upload immediately (Choose files behavior)
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

  // upload a single file to backend using axios and report progress
  const uploadSingle = async (item: UploadFile) => {
    setFiles((prev) =>
      prev.map((p) =>
        p.id === item.id ? { ...p, status: 'submitting', progress: 0 } : p
      )
    );

    // validate file type (backend expects application/pdf)
    if (item.file.type !== 'application/pdf') {
      setFiles((prev) =>
        prev.map((p) => (p.id === item.id ? { ...p, status: 'error' } : p))
      );
      return;
    }

    const form = new FormData();
    form.append('pdf_file', item.file);

    try {
      await axios.post('/upload_pdf', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (ev: any) => {
          // axios progress event shape may vary by version; guard accordingly
          const loaded = ev.loaded ?? ev.progress?.loaded;
          const total = ev.total ?? ev.progress?.total;
          if (!total) return;
          const percent = Math.round((loaded * 100) / total);
          setFiles((prev) =>
            prev.map((p) =>
              p.id === item.id ? { ...p, progress: percent } : p
            )
          );
        },
      });

      // mark as uploaded to backend
      setFiles((prev) =>
        prev.map((p) =>
          p.id === item.id ? { ...p, progress: 100, status: 'uploaded' } : p
        )
      );
      return true;
    } catch (err) {
      console.error('Upload failed', err);
      setFiles((prev) =>
        prev.map((p) => (p.id === item.id ? { ...p, status: 'error' } : p))
      );
      return false;
    }
  };

  const removeFile = (id: string) => {
    setFiles((prev) => prev.filter((f) => f.id !== id));
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      // upload files sequentially and update progress
      const ready = files.filter((f) => f.status === 'done');
      if (ready.length === 0) {
        // nothing ready to send to backend
        alert(
          'No files are ready to submit. Wait until client-side upload finishes (status: done) before submitting.'
        );
        return;
      }

      let uploadedCount = 0;
      for (const f of ready) {
        const ok = await uploadSingle(f);
        if (ok) uploadedCount++;
      }

      if (uploadedCount === 0) {
        alert(
          'Upload failed: could not reach backend or all uploads errored. Check backend availability and try again.'
        );
      } else if (uploadedCount < ready.length) {
        alert(
          `Uploaded ${uploadedCount} of ${ready.length} files. Some uploads failed.`
        );
      } else {
        alert(`Successfully uploaded ${uploadedCount} files to backend.`);
      }
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
