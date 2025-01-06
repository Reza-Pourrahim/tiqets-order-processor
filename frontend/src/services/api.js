import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000/api",
});

export const processOrders = async () => {
  const response = await api.get("/process");
  return response.data;
};

export const getTopCustomers = async () => {
  const response = await api.get("/customers/top");
  return response.data;
};

export const getUnusedBarcodes = async () => {
  const response = await api.get("/barcodes/unused");
  return response.data;
};

export const getCustomerOrders = async (customerId) => {
  const response = await api.get(`/orders/${customerId}`);
  return response.data;
};
