import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { getTopCustomers } from '../services/api';

const TopCustomers = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['topCustomers'],
    queryFn: getTopCustomers
  });

  if (isLoading) return <div>Loading...</div>;

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">Top 5 Customers</h2>
      <div className="space-y-2">
        {data?.data?.map(({ customer_id, ticket_count }) => (
          <div key={customer_id} className="flex justify-between p-2 hover:bg-gray-50">
            <span>Customer {customer_id}</span>
            <span className="font-semibold">{ticket_count} tickets</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TopCustomers;
