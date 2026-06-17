import api from "./api";

export const getTransactions = () => {
  return api.get("/transactions");
};

export const getItemHistory = (id) => {
  return api.get(`/transactions/items/${id}/history`);
}

export const adjustStock = (id, itemData) => {
  return api.post(`/transactions/items/${id}/adjust`, itemData);
}

export const removeStock = (id, itemData) => {
  return api.post(`/transactions/items/${id}/remove`, itemData);
}

export const addStock = (id, itemData) => {
  return api.post(`/transactions/items/${id}/add`, itemData);
}
