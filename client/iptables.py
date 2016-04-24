import iptc


class IPTables(object):
    """
    Sets iptables rule for redirection to specified netfilter queue
    Hardcoded since no need for high configurability for now
    """

    @staticmethod
    def set_rule(chain_name, queue_num):
        """
        Sets an NFQUEUE target for a given chain. The matching packets are forwarded to the queue specified by 'queue_num'
        :param chain_name:      the name of the chain for which to set a new rule
        :param queue_num:       the number of the NFQUEUE to set the forwarding for
        :returns rule:          the object representing the set rule
        """

        rule = iptc.Rule()
        rule.protocol = "tcp"

        tcp_match = rule.create_match("tcp")
        tcp_match.dport = "12345"

        connbytes_match = rule.create_match("connbytes")
        connbytes_match.set_parameter("connbytes-mode", "packets")
        connbytes_match.set_parameter("connbytes-dir", "both")
        connbytes_match.set_parameter("connbytes", "4")

        target = rule.create_target("NFQUEUE")
        target.set_parameter("queue-num", queue_num)

        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain_name)
        chain.insert_rule(rule)

        return rule

    @staticmethod
    def delete_rule(chain_name, rule):
        """
        Removes the rule from the given chain
        :param chain_name:      name of the chain
        :param rule:            object of the rule to be removed
        """

        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain_name)
        chain.delete_rule(rule)
