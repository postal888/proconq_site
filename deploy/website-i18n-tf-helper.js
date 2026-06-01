
function tf(key, params) {
  var s = t(key);
  if (params) {
    Object.keys(params).forEach(function (k) {
      s = s.split('{' + k + '}').join(String(params[k]));
    });
  }
  return s;
}
