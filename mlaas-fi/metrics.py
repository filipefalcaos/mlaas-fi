def confidence_change(conf, alt_conf):
    """
    Computes the change (in percent) in confidence level for a group of base and alternative predictions.

    :param conf: The confidence level of the base prediction
    :param alt_conf: The confidence level of the alternative predictions
    :returns: The confidence change
    """

    return (abs(conf - alt_conf) / conf) * 100.0


def misclassification_rate(preds, alt_preds, k=1):
    """
    Computes the misclassification rate for a group of base and alternative predictions.
    For details, check: Narodytska, Nina, and Shiva Prasad Kasiviswanathan. "Simple black-box
    adversarial perturbations for deep networks." arXiv preprint arXiv:1612.06299 (2016).

    :param preds: The list of base predictions
    :param alt_preds: The list of alternative predictions
    :param k: The number of misclassified predictions to trigger a misclassification
    :returns: The misclassification rate
    """

    n_preds = len(preds)
    n_misclassification = 0

    for i in range(len(preds)):
        if len(preds[i]) == 0:
            n_preds -= 1
            continue
        elif preds[i][0] not in alt_preds[i][:k]:
            n_misclassification += 1

    rate = round(n_misclassification / n_preds, 2)
    return rate
