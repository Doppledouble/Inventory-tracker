import api from "./api";

export const getAssignments = () => {
  return api.get("/assignments");
};

export const getActiveAssignments = () => {
  return api.get("/assignments?active=true");
};

export const getAssignmentById = (id) => {
  return api.get(`/assignments/${id}`);
}

export const createAssignment = (assignmentData) => {
  return api.post("/assignments", assignmentData);
}

export const updateAssignment = (id, assignmentData) => {
  return api.patch(`/assignments/${id}`, assignmentData);
};

export const deleteAssignment = (id) => {
  return api.delete(`/assignments/${id}`);
};

export const returnAssignment = (id) => {
  return api.patch(`/assignments/${id}/return`);
};
