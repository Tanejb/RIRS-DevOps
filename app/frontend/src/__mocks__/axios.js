const axiosMock = {
  get: jest.fn(),
  post: jest.fn(),
  patch: jest.fn(),
  delete: jest.fn(),
  defaults: { headers: { common: {} } },
  create: () => axiosMock,
};

export default axiosMock;

