<?php
/* Common journo-related functions */

require_once '../conf/general';
require_once 'misc.php';
//require_once '../../phplib/db.php';
require_once 'arc2/ARC2.php';


$ns = array(
    'jl' => 'http://'. OPTION_WEB_DOMAIN . '/',
    'rdf'=>"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'rdfs'=>"http://www.w3.org/2000/01/rdf-schema#",
    'foaf'=>"http://xmlns.com/foaf/0.1/",
    'doac'=>"http://ramonantonio.net/content/xml/doac01",
      'dc' => 'http://purl.org/dc/elements/1.1/',
    );
$_conf = array('ns' => $ns);


function journo_asARC2Index( &$journo_data ) {
    extract( $journo_data, EXTR_PREFIX_ALL, 'j' );

    $j = array();
    $j['rdf:type'] = array( 'foaf:Person' );
    $j['foaf:name'] = array( x($j_prettyname) );
    $j['foaf:givenName'] = array( x($j_firstname) );
    $j['foaf:familyName'] = array( x($j_lastname) );

    if( $j_known_email )
        $j['foaf:mbox'] = "mailto:" . x($j_known_email['email']);
    if( $j_phone_number )
        $j['foaf:phone'] = "tel:". x($j_phone_number);

    $webpages = array();
    $blogs = array();
    foreach( $j_links as $l ) {
        switch( $l['kind'] ) {
            case 'webpage': $webpages[] = x($l['url']); break;
            case 'blog': $blogs[] = x($l['url']); break;
        }
    }
    $j['foaf:homepage'] = $webpages;
    $j['foaf:weblog'] = $blogs;


    $experience = array();
    $i=0;
    foreach( $j_employers as $e ) {
        $foo = array(' rdf:type' => 'doac:Experience' );
        if( $e['kind'] == 'freelance' ) {
           $foo['doac:position'] = array( 'Freelance' );
        } else {
           $foo['doac:organisation'] = array( x($e['employer']) );
           $foo['doac:position'] = array( x($e['job_title']) );
        }
        if( $e['year_from'] )
            $foo['doac:date-starts'] = array( $e['year_from'] );
        if( !$e['current'] && $e['year_to'] )
            $foo['doac:date-ends'] = array( $e['year_to'] );
        $ename = "#exp{$i}";
        $experience[$ename] = $foo;
        ++$i;
    }

    $j['doac:experience'] = array();
    foreach( $experience as $ename=>$e ) {
        $j['doac:experience'][] = $ename;
    }


    return array_merge( array( 'jl:'.$j_ref => $j ),
        $experience );
}


function journo_emitRDFXML( &$j ) {
    global $_conf;
    $idx = journo_asARC2Index($j);

    $ser = ARC2::getRDFXMLSerializer($_conf);
    $doc = $ser->getSerializedIndex($idx);

//    var_dump( $idx );
    print $doc;
}


