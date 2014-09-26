;; This sets up run-on-save testing in emacs

(defun transducers-python-tests ()
  (interactive)
  (when (projectile-project-root)
    (let* ((default-directory (projectile-project-root))
	   (buffer-name "*transducers-tests*")
	   (buff (get-buffer-create buffer-name)))
      (display-buffer buff)
      (shell-command (concat "python3 -m unittest discover transducers/test") buff)
      (with-current-buffer buff
	(compilation-mode)))))

(defun transducers-enable-tests ()
  (interactive)
  (add-hook 'after-save-hook 'transducers-python-tests))

(defun transducers-disable-tests ()
  (interactive)
  (remove-hook 'after-save-hook 'transducers-python-tests))

(add-hook 'kill-emacs-hook 'transducers-disable-tests)
(transducers-enable-tests)
