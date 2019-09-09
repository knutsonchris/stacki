# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@


from ariadne import ObjectType, QueryType, MutationType
import app.db as db

query = QueryType()
mutation = MutationType()

# work in progress
@query.field("firewalls")
def resolve_firewalls(
    _, info, scope=None, name=None, table_type=None,chain=None, 
    action=None, service=None, protocol=None, network=None,
    output_network=None, flags=None, comment=None):

    args = ()
    if scope:
        scope_id = db.run_sql("SELECT id FROM scope_map WHERE scope=%s", scope)
        args += (f'scope_map_id="{scope_id}"')

    where = "WHERE"
    if name:
        args += (name,)
        where += " name=%s"
    
    if table_type:
        args += (table_type, )
        where += "table_type=%s"
    
    if chain:
        args += (chain,)
        where += "chain=%s"

    if action:
        args += (f'action="{action}"')

    if service:
        args += (f'service="{service}"')
    
    if protocol:
        args += (f'protocol="{protocol}"')
    
    if network:
        # TODO lookup in_subnet_id shenanigans
        pass
    
    if output_network:
        # TODO lookup out_subnet_id shenanigans
        pass

    if flags:
        args += (f'flags="{flags}"')

    if comment:
        args += (f"comment='{comment}'")

    where_string = "AND".join(where)


    results, _ = db.run_sql("SELECT id, scope_map_id, name, table_type, chain, action, service, protocol, in_subnet_id, out_subnet_id, flags, comment FROM firewall_rules", args2)

    return results


"""
@mutation.field("addAppliance")
def resolve_add_appliance(_, info, name, public="no"):
    # TODO: Maybe make the appliance names unique in the db
    # TODO: Add kickstartable and managed attrs

    cmd = "INSERT INTO appliances (name, public) VALUES (%s, %s)"
    args = (name, public)
    db.run_sql(cmd, args)

    cmd = "SELECT id, name, public FROM appliances WHERE name=%s"
    args = (name,)
    result, _ = db.run_sql(cmd, args, fetchone=True)

    return result


@mutation.field("updateAppliance")
def resolve_update_appliance(_, info, id, name=None, public=None):
    # TODO: Maybe make the appliance names unique in the db
    # TODO: Check if the name collides

    cmd = "SELECT id, name, public FROM appliances WHERE id=%s"
    args = (id,)
    appliance, _ = db.run_sql(cmd, args, fetchone=True)
    if not appliance:
        raise Exception("No appliance found")

    if not name and not public:
        return appliance

    update_params = []
    args = ()
    if name:
        update_params.append("name=%s")
        args += (name,)

    if public is not None:
        update_params.append("public=%s")
        args += (public,)

    args += (id,)
    cmd = f'UPDATE appliances SET {", ".join(update_params)}' + " WHERE id=%s"
    db.run_sql(cmd, args)

    cmd = "SELECT id, name, public FROM appliances WHERE id=%s"
    args = (id,)
    result, _ = db.run_sql(cmd, args, fetchone=True)

    return result


@mutation.field("deleteAppliance")
def resolve_delete_appliance(_, info, id):

    cmd = "DELETE FROM appliances WHERE id=%s"
    args = (id,)
    _, affected_rows = db.run_sql(cmd, args)

    if not affected_rows:
        return False

    return True

"""

object_types = []
