---
layout: post
title: How does react-hooks work?
date: 2020-01-31 10:18:00
tags: technology
---

SOURCE:

- [https://reactjs.org/docs/hooks-intro.html](https://reactjs.org/docs/hooks-intro.html)
- [https://www.youtube.com/watch?v=dpw9EHDh2bM&feature=emb_logo](https://www.youtube.com/watch?v=dpw9EHDh2bM&feature=emb_logo)
- [https://medium.com/@morgler/dont-use-redux-9e23b5381291](https://medium.com/@morgler/dont-use-redux-9e23b5381291)
- [https://www.newline.co/@CarlMungazi/a-journey-through-the-usestate-hook--a4983397](https://www.newline.co/@CarlMungazi/a-journey-through-the-usestate-hook--a4983397)

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/reactlifecycle.png)</span>

Why react-hooks?

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/reacthooks.png)</span>

To avoid developers introducing too much abstraction with a separate state management library (redux, mobx…) that often requires to jump between different files, write excessive amounts of code and lose time. the facebook team invented react hooks in 2015. 

```javascript
const ComponentWithHook = () => {
  const [count, setCount] = React.useState(0);
  const [bool, setBool] = React.useState(false);

  React.useEffect(() => {}, [count, bool]);
  const child = React.useRef();

  return <button onClick={() => setCount(count + 1)}>Count: {count}</button>;
};

ReactDOM.render(<ComponentWithHook />, document.getElementById("root"));
```


```javascript
{
  memoizedState: 0, // the setCount hook
  baseState: 0,
  queue: { /* ... */},
  baseUpdate: null,
  next: { // the setBool hook
    memoizedState: false,
    baseState: false,
    queue: { /* ... */},
    baseUpdate: null,
    next: { // the useEffect hook
      memoizedState: {
        tag: 192,
        create: () => {},
        destory: undefined,
        deps: [0, false],
        next: { /* ... */}
      },
      baseState: null,
      queue: null,
      baseUpdate: null,
      next: { // the useRef hook
        memoizedState: {
          current: undefined
        },
        baseState: null,
        queue: null,
        baseUpdate: null,
      }
    }
  }
}
```

Hooks creates on the first render, a linked list of mutable fiber objects to represent the entire DOM. It holds the states that preserves from re-renders and store the data of a component. It also has a reference that points to the next node of the tree. 