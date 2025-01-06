import { useQuery } from "@tanstack/react-query";
import React from "react";
import TopCustomers from "../components/TopCustomers";
import UnusedBarcodes from "../components/UnusedBarcodes";
import { processOrders } from "../services/api";

const Dashboard = () => {
  const { data: processedData, isLoading: isProcessing } = useQuery({
    queryKey: ["process"],
    queryFn: processOrders,
  });

  if (isProcessing) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg">Processing orders...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <TopCustomers />
        <UnusedBarcodes />
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Processed Orders</h2>
        <div className="space-y-4">
          {processedData?.data?.orders.map((order) => (
            <div key={order.order_id} className="border-b pb-4">
              <div className="flex justify-between items-center">
                <div>
                  <p className="font-semibold">Order ID: {order.order_id}</p>
                  <p className="text-gray-600">
                    Customer ID: {order.customer_id}
                  </p>
                </div>
                <div className="text-sm text-gray-500">
                  {order.barcodes.length} tickets
                </div>
              </div>
              <div className="mt-2 text-sm text-gray-500">
                Barcodes: {order.barcodes.join(", ")}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
