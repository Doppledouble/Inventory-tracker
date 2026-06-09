import api from "./api";

export const getItems = () => {
  return api.get("/items");
};

export const getItemById = (id) => {
  return api.get(`/items/${id}`);
}

export const createItem = (itemData) => {
  return api.post("/items", itemData);
}

export const updateItem = (id, itemData) => {
  return api.patch(`/items/${id}`, itemData);
};

export const deleteItem = (id) => {
  return api.delete(`/items/${id}`);
};
