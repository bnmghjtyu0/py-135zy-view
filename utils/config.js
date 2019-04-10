// 過濾相同的
const dedupeByProperty = (arr, objKey) => {
  return arr.reduce(
    (acc, curr) =>
      acc.some(a => a[objKey] === curr[objKey]) ? acc : [...acc, curr],
    []
  );
};
