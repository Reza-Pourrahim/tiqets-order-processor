import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { getUnusedBarcodes } from '../services/api';

const UnusedBarcodes = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['unusedBarcodes'],
    queryFn: getUnusedBarcodes
  });

  if (isLoading) return <div>Loading...</div>;

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">Unused Barcodes</h2>
      <div className="text-lg mb-4">
        Total: {data?.data?.count || 0}
      </div>
      <div className="space-y-2">
        {data?.data?.barcodes?.map(({ barcode }) => (
          <div key={barcode} className="p-2 hover:bg-gray-50">
            {barcode}
          </div>
        ))}
      </div>
    </div>
  );
};

export default UnusedBarcodes;
