#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Processor functions
"""
from rebulk.utils import IdentitySet


def initiator(match):
    """
    Retrieve the initiator parent of a match
    :param match:
    :type match:
    :return:
    :rtype:
    """
    while match.parent:
        match = match.parent
    return match


def conflict_prefer_longer(matches):
    """
    Remove shorter matches if they conflicts with longer ones

    :param matches:
    :type matches: rebulk.match.Matches
    :param context:
    :type context:
    :return:
    :rtype: list[rebulk.match.Match]
    """
    to_remove_matches = IdentitySet()
    for match in filter(lambda match: not match.private, matches):
        conflicting_matches = IdentitySet()

        for i in range(*match.span):
            conflicting_matches.update(matches.starting(i))
            if i != match.span[0]:
                conflicting_matches.update(matches.ending(i))

        conflicting_matches.remove(match)
        if conflicting_matches:
            # keep the match only if it's the longest
            for conflicting_match in filter(lambda match: not match.private, conflicting_matches):
                if len(initiator(conflicting_match)) < len(initiator(match)):
                    to_remove_matches.add(conflicting_match)

    for match in to_remove_matches:
        matches.remove(match)

    return matches


def remove_private(matches):
    """
    Removes private matches.

    :param matches:
    :type matches:
    :return:
    :rtype:
    """
    for match in list(matches):
        if match.private:
            matches.remove(match)

    return matches
