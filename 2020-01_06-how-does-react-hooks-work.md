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

React hooks has been created to avoid developers introducing too much abstraction with a separate state management library (redux, mobx...). That often requires to jump between different files, write excessive amounts of code and lose time.

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

ComponentWithHook is a function which returns an object (all JXS calls are translated into objects by this babel plugin). On the first render of a component, a linked list of the Hooks called gets created.

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

Hooks are stored according to their calling order in a linked list of fiber objects to represent the entire DOM. A fiber is an object that is mutable and holds component state that preserves from re-renders. Every component has a corresponding fiber object. Each node has its data and also a reference that points to the next node in the list. The order of nodes is entirely dependent on each node’s reference to the next.
