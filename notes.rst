;;transducer signature
(whatever, input -> whatever) -> (whatever, input -> whatever)

;;look Ma, no collection!
(map f)

returns a 'mapping' transducer. filter et al get similar support.

You can build a 'stack' of transducers using ordinary function composition (comp):

This arity will return a transducer that represents the same logic,
independent of lazy sequence processing.

(def xform (comp (map inc) (filter even?)))

(defn mapping [f]
   (fn [f1]
     (fn [result input]
       (f1 result (f input)))))

 (defn filtering [pred]
   (fn [f1]
     (fn [result input]
       (if (pred input)
         (f1 result input)
         result))))

 (defn mapcatting [f]
   (fn [f1]
     (fn [result input]
       (reduce f1 result (f input)))))

(reduce + 0 (map inc [1 2 3 4]))
;;becomes
(reduce ((mapping inc) +) 0 [1 2 3 4])
