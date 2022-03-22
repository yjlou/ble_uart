//  Utilities

// Returns a closure object that encapsulate a 'self' for 'func'.
//
// This is useful to closure a class function with an object reference.
//
function make_func(func, self) {
  function closure(para0, para1, para2, para3, para4, para5, para6, para7) {
    func(self, para0, para1, para2, para3, para4, para5, para6, para7);
  }
  return closure;
}

