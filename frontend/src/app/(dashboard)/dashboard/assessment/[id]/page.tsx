'use client';
import React, { useEffect, useState } from 'react';

import { fetchAssesment } from '@/lib/api';
import { toast } from 'react-toastify';
import { useRouter, useParams } from 'next/navigation';
import { useAuth } from '@/lib/AuthContext';
import { generateAssessmentPdf } from '@/lib/generatePDF'; // 👈 Import your PDF function

const AssessmentView = () => {
  const router = useRouter();
  const { token } = useAuth();
  const params = useParams();
  const idParam = params.id;
  const id = typeof idParam === 'string' ? parseInt(idParam) : NaN;

  const [data, setData] = useState<any>(null);

  useEffect(() => {
    if (id && token) {
      fetchAssesment(id, token)
        .then((data) => setData(data))
        .catch(() => toast.error("Failed to fetch assessment"));
    }
  }, [id, token]);

  const handleDownloadPdf = () => {
    if (data) {
      generateAssessmentPdf(data); // 👈 Call your PDF generator here
    } else {
      toast.warn("Assessment data not loaded yet.");
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Assessment View</h1>
      
      <button
        onClick={handleDownloadPdf}
        className="mb-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Download PDF
      </button>

      <pre className="bg-gray-100 p-4 rounded text-sm overflow-x-auto">
        {data ? JSON.stringify(data, null, 2) : "Loading..."}
      </pre>
    </div>
  );
};

export default AssessmentView;
